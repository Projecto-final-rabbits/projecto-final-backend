from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

from src.config.database import SessionLocal
from src.infrastructure.db.models.bodega_model import Producto
from src.application.schemas.bodegas import ProductoCreate, ProductoRead
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepository
from src.application.services.proveedores_service import proveedor_existe

from src.application.services.productos_service import ProductosService
from src.infrastructure.adapters.out.pubsub_event_publisher import PubsubEventPublisher
from src.config.database import get_db
from typing import Optional

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoRead)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    if not proveedor_existe(producto.proveedor_id):
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    repo = ProductoRepository(db)
    nuevo = Producto(**producto.dict())
    creado = repo.crear(nuevo)

    event_publisher = PubsubEventPublisher()
    productos_service = ProductosService(event_publisher, repo)
    creado_schema = ProductoRead.from_orm(creado)

    try:
        productos_service.crear_producto(creado_schema.dict())
    except Exception as e:
        print(f"⚠️ Error al publicar el evento de creación de producto: {e}")
        
    return creado

@router.get("/", response_model=list[ProductoRead])
def listar_productos(proveedor_id: Optional[int] = None, db: Session = Depends(get_db)):
    repo = ProductoRepository(db)
    if proveedor_id:
        return repo.obtener_por_proveedor(proveedor_id)
    else:
        return repo.obtener_todos()

@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    repo = ProductoRepository(db)
    producto = repo.obtener_por_id(str(producto_id))
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    repo = ProductoRepository(db)
    exito = repo.eliminar(str(producto_id))
    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}

@router.post("/masivo")
async def cargar_csv_productos(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    content = await file.read()

    repo = ProductoRepository(db)
    event_publisher = PubsubEventPublisher()
    productos_service = ProductosService(event_publisher, repo)

    resultado = productos_service.crear_productos_desde_csv(content)

    return JSONResponse(status_code=201, content=resultado)
