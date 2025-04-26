# src/main.py

import os
import threading
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.ventas_routes import router as ventas_router
from src.api.routes.productos_routes import router as productos_router
from src.api.routes.clientes_routes import router as clientes_router
from src.api.routes.vendedores_routes import router as vendedores_router
from src.api.routes.pedidos_routes import router as pedidos_router
from src.api.routes.detalles_routes import router as detalles_router
from src.api.routes.planes_venta_routes import router as planes_venta_router

from src.config.database import Base, engine
from src.infrastructure.messaging.pubsub import PubSubSubscriber

# Carga .env
load_dotenv("src/.env")

app = FastAPI()

# Routers
app.include_router(ventas_router)
app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(vendedores_router)
app.include_router(pedidos_router)
app.include_router(detalles_router)
app.include_router(planes_venta_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

if os.getenv("TESTING") != "true":
    from src.infrastructure.messaging.pubsub import PubSubSubscriber
    from src.infrastructure.messaging.handlers import handle_product_created
    print("🚀 Iniciando suscripción a Pub/Sub desde VENTAS")
    pubsub = PubSubSubscriber()
    pubsub.subscribe_to_productos(callback=handle_product_created)

@app.on_event("startup")
def on_startup():
    # 1) Inicializar la base de datos
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")

    # 2) Arrancar el subscriber de productos
  
    print("🚀 Subscriber de productos iniciado.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)
