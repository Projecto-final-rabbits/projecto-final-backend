from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.compras_routes import router as compras_router
from src.api.routes.proveedores_routes import router as proveedores_router
from src.api.routes.productos_routes import router as productos_router
from src.api.routes.ordenes_routes import router as ordenes_router
from src.api.routes.detalles_routes import router as detalles_router

import os

from src.config.database import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

if os.getenv("TESTING") != "true":
    from src.infrastructure.messaging.pubsub import subscribe_to_topic
    from src.infrastructure.messaging.handlers import handle_product_created
    print("🚀 Iniciando suscripción a Pub/Sub desde COMPRAS")
    subscribe_to_topic(callback=handle_product_created)

app.include_router(compras_router)
app.include_router(proveedores_router)
app.include_router(productos_router)
app.include_router(ordenes_router)
app.include_router(detalles_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.on_event("startup")
def on_startup():
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")