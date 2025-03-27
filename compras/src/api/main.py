from fastapi import FastAPI
from src.api.routes.compras_routes import router as compras_router

from src.config.database import Base, engine
from src.infrastructure.db.models.compra_model import CompraModel

app = FastAPI()

app.include_router(compras_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.on_event("startup")
def on_startup():
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")