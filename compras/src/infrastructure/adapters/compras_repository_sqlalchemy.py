from typing import List
from src.application.ports.compras_repository import CompraRepository
from src.domain.models.compra import Compra
from src.infrastructure.db.models.compra_model import CompraModel
from src.config.database import SessionLocal

class CompraRepositorySQLAlchemy(CompraRepository):
    def guardar(self, compra: Compra) -> Compra:
        with SessionLocal() as session:
            db_compra = CompraModel(
                producto=compra.producto,
                cantidad=compra.cantidad,
                proveedor=compra.proveedor
            )
            session.add(db_compra)
            session.commit()
            session.refresh(db_compra)
            return Compra(
                producto=db_compra.producto,
                cantidad=db_compra.cantidad,
                proveedor=db_compra.proveedor
            )

    def listar_todas(self) -> List[Compra]:
        with SessionLocal() as session:
            compras_orm = session.query(CompraModel).all()
            return [Compra(c.producto, c.cantidad, c.proveedor) for c in compras_orm]