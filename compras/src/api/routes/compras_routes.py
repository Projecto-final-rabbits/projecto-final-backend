from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi.responses import JSONResponse

from src.infrastructure.adapters.compras_repository_sqlalchemy import CompraRepositorySQLAlchemy
from src.domain.models.compra import Compra
from src.api.schemas.compra_schema import CompraOut, CompraCreate

router = APIRouter()
repo = CompraRepositorySQLAlchemy()

@router.post("/compras", response_model=CompraOut)
def crear_compra(compra: CompraCreate):
    nueva_compra = Compra(
        producto=compra.producto,
        cantidad=compra.cantidad,
        proveedor=compra.proveedor
    )
    compra_guardada = repo.guardar(nueva_compra)

    # Simular ID asignado (por ahora)
    return CompraOut(id=1, **vars(compra_guardada))

@router.get("/compras", response_model=List[CompraOut])
def listar_compras():
    compras = repo.listar_todas()
    return [
        CompraOut(id=i + 1, **vars(c))  # Simulación de IDs por ahora
        for i, c in enumerate(compras)
    ]

@router.get("/health")
def healthcheck():
    return JSONResponse(content={"message": "OK"}, status_code=200)