from src.application.schemas.bodegas import ProductoCreate, ProductoRead
from src.infrastructure.db.models.bodega_model import Producto
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepository
from src.application.services.proveedores_service import proveedor_existe
from fastapi import HTTPException
import pandas as pd
import numpy as np
import io

class ProductosService:
    def __init__(self, event_publisher, repo: ProductoRepository):
        self.event_publisher = event_publisher
        self.repo = repo

    def crear_producto(self, producto: dict):
        from src.domain.events.event_type import EventType
        self.event_publisher.publish(EventType.product_created, producto)

    def crear_productos_desde_csv(self, content: bytes):
        try:
            df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al leer el archivo CSV: {e}")

        if 'fecha_vencimiento' in df.columns:
            df['fecha_vencimiento'] = pd.to_datetime(df['fecha_vencimiento'], errors='coerce')

        df = df.replace({np.nan: None, pd.NaT: None})

        productos_creados = []
        errores = []

        for index, row in df.iterrows():
            try:
                producto_data = row.to_dict()
                producto_schema = ProductoCreate(**producto_data)

                if not proveedor_existe(producto_schema.proveedor_id):
                    errores.append({
                        "fila": index + 2,
                        "error": f"Proveedor {producto_schema.proveedor_id} no encontrado"
                    })
                    continue

                nuevo = Producto(**producto_schema.dict())
                creado = self.repo.crear(nuevo)
                creado_schema = ProductoRead.from_orm(creado)

                try:
                    self.crear_producto(creado_schema.dict())
                except Exception as e_pub:
                    errores.append({
                        "fila": index + 2,
                        "error": f"Producto creado localmente pero falló PubSub: {e_pub}"
                    })
                    continue

                productos_creados.append(creado_schema.id)

            except Exception as e:
                errores.append({
                    "fila": index + 2,
                    "error": f"Error al procesar fila: {e}"
                })

        return {
            "mensaje": f"Se procesaron {len(df)} productos",
            "creados": len(productos_creados),
            "fallos": len(errores),
            "errores": errores
        }
