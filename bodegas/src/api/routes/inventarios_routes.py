from fastapi import APIRouter, Depends
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