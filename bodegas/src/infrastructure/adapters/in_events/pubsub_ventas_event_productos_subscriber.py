# src/infrastructure/handlers/ventas_productos_handler.py
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from src.config.database import engine
from src.infrastructure.adapters.inventario_repository_sqlalchemy import InventarioRepository

class VentasProductosHandler:
    def __call__(self, payload: Dict) -> None:
        productos: List[dict] = payload.get("productos", [])
        logging.info(f"🟢 Recibido pedido con {len(productos)} ítems")

        with Session(engine) as db:
            invent_repo = InventarioRepository(db)

            for p in productos:
                pid = p.get("producto_id")
                try:
                    cantidad = int(p.get("cantidad", 0))
                except (TypeError, ValueError):
                    raise HTTPException(
                        status_code=422,
                        detail=f"Cantidad inválida para producto {pid}"
                    )

                try:
                    invent_repo.descontar_stock(pid, cantidad)
                except ValueError as err:
                    msg = str(err)
                    if msg.startswith("No existe inventario"):
                        raise HTTPException(status_code=404, detail=msg)
                    if msg.startswith("Stock insuficiente"):
                        raise HTTPException(status_code=409, detail=msg)
                    # genérica
                    raise HTTPException(status_code=400, detail=msg)

            db.commit()
            logging.info("🟢 Stock descontado correctamente")