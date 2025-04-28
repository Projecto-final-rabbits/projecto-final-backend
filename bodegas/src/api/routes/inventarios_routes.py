from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.infrastructure.adapters.inventario_repository_sqlalchemy import InventarioRepository
from src.application.schemas.bodegas import InventarioRead

router = APIRouter(prefix="/inventarios", tags=["Inventarios"])

@router.get("/", response_model=List[InventarioRead])
def listar_inventarios(db: Session = Depends(get_db)):
    repo = InventarioRepository(db)
    return repo.obtener_todos()

# --- nueva ruta: inventario por producto ---
@router.get(
    "/producto/{producto_id}",
    response_model=InventarioRead,
    summary="Obtener inventario por producto UUID"
)
def obtener_inventario_por_producto(
    producto_id: UUID,
    db: Session = Depends(get_db)
):
    repo = InventarioRepository(db)
    # el repositorio almacena el producto_id como str
    inventario = repo.obtener_por_producto(str(producto_id))
    if not inventario:
        raise HTTPException(
            status_code=404,
            detail=f"No existe inventario para el producto {producto_id}"
        )
    return inventario