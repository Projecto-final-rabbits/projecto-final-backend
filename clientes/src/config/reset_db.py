# reset_db.py
from src.config.database import Base, engine

# ¡Ojo! Esto DROPEA todas las tablas y las vuelve a crear según tus modelos
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ Tablas recreadas con el esquema actualizado")
