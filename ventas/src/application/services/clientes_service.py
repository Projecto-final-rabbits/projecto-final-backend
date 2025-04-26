import httpx
import os
from dotenv import load_dotenv
from src.infrastructure.adapters.cliente_repository_sqlalchemy import ClienteRepositorySQLAlchemy
from sqlalchemy.orm import Session
from src.config.database import get_db
from fastapi import Depends

load_dotenv("src/.env")

CLIENTES_BASE_URL = os.getenv("CLIENTES_BASE_URL")

from src.config.database import SessionLocal

def cliente_existe(cliente_id: int) -> bool:
    db = SessionLocal()
    try:
        repo = ClienteRepositorySQLAlchemy(db)
        cliente = repo.obtener_por_id(cliente_id)
        return cliente is not None
    except Exception as e:
        print(f"🚨 Error al verificar cliente: {e}")
        return False
    finally:
        db.close()
