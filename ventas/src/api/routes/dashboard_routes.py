from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from src.config.database import SessionLocal
from src.application.schemas.dashboard import SalesSummaryRead
from src.application.services.dashboard_service import obtener_resumen_ventas

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sales-summary", response_model=SalesSummaryRead)
def sales_summary(
    start_date: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD), defecto: inicio del mes actual"),
    end_date: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD), defecto: fin del mes actual"),
    db: Session = Depends(get_db),
):
    try:
        summary = obtener_resumen_ventas(start_date, end_date, db)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
