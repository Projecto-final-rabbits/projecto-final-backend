import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Determinar si estamos en entorno de testing
is_testing = os.getenv("TESTING") == "true" or os.getenv("PYTEST_CURRENT_TEST")

# Cargar archivo .env solo en desarrollo o testing
if is_testing or os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Seleccionar la URL de conexión adecuada
if is_testing:
    database_url = "sqlite:///./test.db"
    connect_args = {"check_same_thread": False}
else:
    database_url = os.getenv("DATABASE_URL")
    connect_args = {}

# Validar que haya URL de conexión en producción
if not database_url:
    raise ValueError("DATABASE_URL compras no está definido en el entorno")

# Crear motor y sesión
engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
