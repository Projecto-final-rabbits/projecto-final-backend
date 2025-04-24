from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.bodegas_routes import router as bodegas_router
from src.api.routes.productos_routes import router as productos_router
from src.api.routes.movimientos_routes import router as movimientos_router
from src.api.routes.inventarios_routes import router as inventario_router

from src.config.database import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(bodegas_router)
app.include_router(productos_router)
app.include_router(movimientos_router)
app.include_router(inventario_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)

@app.on_event("startup")
def on_startup():
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")