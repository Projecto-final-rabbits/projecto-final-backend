from src.application.schemas.ventas import ProductoCreate
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepositorySQLAlchemy
from sqlalchemy.orm import Session

class ProductoEventService:
    def __init__(self, repo: ProductoRepositorySQLAlchemy):
        self.repo = repo

    def crear_producto_desde_evento(self, db: Session, data: dict):
        producto_dto = ProductoCreate(**data)
        return self.repo.guardar(db, producto_dto)
