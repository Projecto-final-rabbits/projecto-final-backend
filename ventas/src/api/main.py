from fastapi import FastAPI
from src.api.routes.ventas_routes import router as ventas_router
from src.api.routes.productos_routes import router as productos_router
from src.api.routes.clientes_routes import router as clientes_router
from src.api.routes.vendedores_routes import router as vendedores_router
from src.api.routes.pedidos_routes import router as pedidos_router
from src.api.routes.detalles_routes import router as detalles_router
from src.api.routes.planes_venta_routes import router as planes_venta_router

# comment
from src.config.database import Base, engine

app = FastAPI()

app.include_router(ventas_router)
app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(vendedores_router)
app.include_router(pedidos_router)
app.include_router(detalles_router)
app.include_router(planes_venta_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

@app.on_event("startup")
def on_startup():
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")