from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.application.schemas.bodegas import MovimientoInventarioCreate, MovimientoInventarioRead, TrasladoInventarioCreate
from src.application.services.movimientos_service import registrar_entrada_producto_service, registrar_salida_producto_service, registrar_traslado_producto_service
from src.infrastructure.adapters.movimiento_repository_sqlalchemy import MovimientoInventarioRepository
from src.config.database import get_db

router = APIRouter(prefix="/movimientos", tags=["Movimientos Inventario"])

@router.post("/entrada", response_model=MovimientoInventarioRead, status_code=status.HTTP_201_CREATED)
def registrar_entrada_producto(movimiento_data: MovimientoInventarioCreate, db: Session = Depends(get_db)):
    return registrar_entrada_producto_service(movimiento_data, db)

@router.get("/", response_model=List[MovimientoInventarioRead])
def listar_movimientos(db: Session = Depends(get_db)):
    repo = MovimientoInventarioRepository(db)
    return repo.obtener_todos()

@router.post("/salida", response_model=MovimientoInventarioRead, status_code=status.HTTP_201_CREATED)
def registrar_salida_producto(movimiento_data: MovimientoInventarioCreate, db: Session = Depends(get_db)):
    return registrar_salida_producto_service(movimiento_data, db)

@router.post("/traslado", response_model=MovimientoInventarioRead, status_code=status.HTTP_201_CREATED)
def registrar_traslado_producto(traslado_data: TrasladoInventarioCreate, db: Session = Depends(get_db)):
    return registrar_traslado_producto_service(traslado_data, db)