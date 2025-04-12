from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/health")
def healthcheck():
    return JSONResponse(content={"message": "OK Sustentacion activa"}, status_code=200)
