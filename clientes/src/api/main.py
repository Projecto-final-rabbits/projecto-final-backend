from fastapi import FastAPI
from src.api.routes.cliente_route import router as clientes_router
from src.api.routes.contacto_cliente_route import router as contactos_router
from src.api.routes.direccion_entrega_route import router as direcciones_router
from src.api.routes.tienda_route import router as tiendas_router
from src.api.routes.pedido_route import router as pedidos_router

from src.config.database import Base, engine

app = FastAPI()

# Incluir todos los routers de los módulos correspondientes
app.include_router(clientes_router)
app.include_router(contactos_router)
app.include_router(direcciones_router)
app.include_router(tiendas_router)
app.include_router(pedidos_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

@app.on_event("startup")
def on_startup():
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")
