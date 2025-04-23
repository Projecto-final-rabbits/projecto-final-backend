from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session

from src.infrastructure.adapters.bodega_repository_sqlalchemy import BodegaRepository
from src.application.schemas.bodegas import BodegaCreate, BodegaRead
from src.infrastructure.db.models.bodega_model import Bodega
from src.config.database import get_db

router = APIRouter(prefix="/bodegas", tags=["Bodegas"])

@router.get("/health")
def healthcheck():
    return JSONResponse(content={"message": "OK Sustentacion activa"}, status_code=200)

@router.get("/", response_model=List[BodegaRead])
def listar_bodegas(db: Session = Depends(get_db)):
    repo = BodegaRepository(db)
    return repo.obtener_todas()

@router.get("/{bodega_id}", response_model=BodegaRead)
def obtener_bodega(bodega_id: int, db: Session = Depends(get_db)):
    repo = BodegaRepository(db)
    bodega = repo.obtener_por_id(bodega_id)
    if not bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    return bodega

@router.post("/", response_model=BodegaRead, status_code=status.HTTP_201_CREATED)
def crear_bodega(bodega: BodegaCreate, db: Session = Depends(get_db)):
    repo = BodegaRepository(db)
    nueva_bodega = Bodega(**bodega.dict())
    return repo.crear(nueva_bodega)

@router.delete("/{bodega_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_bodega(bodega_id: int, db: Session = Depends(get_db)):
    repo = BodegaRepository(db)
    bodega = repo.obtener_por_id(bodega_id)
    if not bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    repo.eliminar(bodega_id)
    return