from src.config.database import Base, engine
from src.infrastructure.db.models.compra_model import CompraModel

def init_db():
    print("⏳ Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente.")

if __name__ == "__main__":
    init_db()