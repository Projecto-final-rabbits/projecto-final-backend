from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.plan_venta_repository_sqlalchemy import PlanVentaRepositorySQLAlchemy
from src.application.schemas.ventas import PlanVentaCreate, PlanVentaRead

router = APIRouter(prefix="/planes-venta", tags=["Planes de Venta"])
repo = PlanVentaRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlanVentaRead)
def crear_plan(plan: PlanVentaCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, plan)

@router.get("/", response_model=List[PlanVentaRead])
def listar_planes(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{plan_id}", response_model=PlanVentaRead)
def obtener_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = repo.obtener_por_id(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de venta no encontrado")
    return plan

@router.delete("/{plan_id}")
def eliminar_plan(plan_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, plan_id)
