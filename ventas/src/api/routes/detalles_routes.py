
from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.detalle_repository_sqlalchemy import DetallePedidoRepositorySQLAlchemy
from src.application.schemas.ventas import DetallePedidoConProducto, DetallePedidoCreate, DetallePedidoRead
from src.application.services.bodega_service import fetch_producto


router = APIRouter(prefix="/detalles", tags=["Detalles de Pedido"])
repo = DetallePedidoRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DetallePedidoRead)
def crear_detalle(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, detalle)

@router.delete("/{detalle_id}")
def eliminar_detalle(detalle_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, detalle_id)

@router.get(
    "/",
    response_model=List[DetallePedidoConProducto],
    summary="Listar todos los detalles con info de producto"
)
def listar_detalles_con_producto(db: Session = Depends(get_db)):
    detalles = repo.listar_todos(db)
    resultado = []
    for det in detalles:
        try:
            producto = fetch_producto(det.producto_id)
        except httpx.HTTPStatusError:
            raise HTTPException(502, detail=f"No se pudo obtener producto {det.producto_id}")
        resultado.append(
            DetallePedidoConProducto(
                id=det.id,
                pedido_id=det.pedido_id,
                producto_id=det.producto_id,
                cantidad=det.cantidad,
                precio_unitario=det.precio_unitario,
                producto=producto
            )
        )
    return resultado

@router.get(
    "/{detalle_id}",
    response_model=DetallePedidoConProducto,
    summary="Obtener un detalle con info de producto"
)
def obtener_detalle_con_producto(detalle_id: int, db: Session = Depends(get_db)):
    det = repo.obtener_por_id(db, detalle_id)
    if not det:
        raise HTTPException(404, detail="Detalle no encontrado")
    try:
        producto = fetch_producto(det.producto_id)
    except httpx.HTTPStatusError:
        raise HTTPException(502, detail=f"No se pudo obtener producto {det.producto_id}")
    return DetallePedidoConProducto(
        id=det.id,
        pedido_id=det.pedido_id,
        producto_id=det.producto_id,
        cantidad=det.cantidad,
        precio_unitario=det.precio_unitario,
        producto=producto
    )