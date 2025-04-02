from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from src.config.database import SessionLocal
from src.infrastructure.db.models.bodega_model import Producto
from src.application.schemas.bodegas import ProductoCreate, ProductoRead
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepository
from src.application.services.proveedores_service import proveedor_existe

from src.application.services.productos_service import ProductosService
from src.infrastructure.adapters.out.pubsub_event_publisher import PubsubEventPublisher


router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductoRead)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    if not proveedor_existe(producto.proveedor_id):
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    repo = ProductoRepository(db)
    nuevo = Producto(**producto.dict())
    creado = repo.crear(nuevo)

    event_publisher = PubsubEventPublisher()
    productos_service = ProductosService(event_publisher)
    creado_schema = ProductoRead.from_orm(creado)
    productos_service.crear_producto(creado_schema.dict())
    return creado

@router.get("/", response_model=list[ProductoRead])
def listar_productos(db: Session = Depends(get_db)):
    repo = ProductoRepository(db)
    return repo.obtener_todos()

@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    repo = ProductoRepository(db)
    producto = repo.obtener_por_id(str(producto_id))
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    repo = ProductoRepository(db)
    exito = repo.eliminar(str(producto_id))
    if not exito:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
