from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.detalle_repository_sqlalchemy import DetallePedidoRepositorySQLAlchemy
from src.application.schemas.ventas import DetallePedidoCreate, DetallePedidoRead, VentaProductoItem, VentaReporte
from src.infrastructure.db.models.venta_model import Cliente

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

@router.get("/", response_model=List[DetallePedidoRead])
def listar_detalles(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{detalle_id}", response_model=DetallePedidoRead)
def obtener_detalle(detalle_id: int, db: Session = Depends(get_db)):
    detalle = repo.obtener_por_id(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.delete("/{detalle_id}")
def eliminar_detalle(detalle_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, detalle_id)

@router.get(
    "/clientes/{cliente_id}/ventas",
    response_model=VentaReporte,
    summary="Reporte de ventas por cliente"
)
def reporte_ventas_cliente(
    cliente_id: int,
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    # 1) Validar existencia de cliente
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 2) Obtener datos agregados
    resultados = repo.ventas_por_cliente(db, cliente_id, fecha_inicio, fecha_fin)

    # 3) Mapear a esquema
    detalle = [
        VentaProductoItem(
            nombre=nombre,
            cantidad_total=cantidad_total,
            total_ventas=total_ventas
        )
        for nombre, cantidad_total, total_ventas in resultados
    ]

    # 4) Devolver reporte
    return VentaReporte(
        cliente_id=cliente_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        detalle=detalle
    )