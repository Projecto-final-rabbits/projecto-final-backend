from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.adapters.in_events.pubsub_ventas_event_productos_subscriber import VentasProductosHandler
from src.infrastructure.messaging.pubsub_ventas_productos_subscriber import PubSubVentasProductosSubscriber
from src.api.routes.bodegas_routes import router as bodegas_router
from src.api.routes.productos_routes import router as productos_router

# comment
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

def _start_pubsub_listener() -> None:
    handler = VentasProductosHandler()
    subscriber = PubSubVentasProductosSubscriber(callback=handler)
    # Arrancamos en daemon para que no bloquee el servidor HTTP
    subscriber.start(daemon=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
    subscriber = PubSubVentasProductosSubscriber(callback=VentasProductosHandler())
    subscriber.start(daemon=False)

@app.on_event("startup")
def on_startup():
    print("🔧 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas listas.")
        # 2. Arrancar Pub/Sub listener
    _start_pubsub_listener()
    print("🚀 Pub/Sub listener iniciado.")