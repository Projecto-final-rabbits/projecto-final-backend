from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
def healthcheck():
    return JSONResponse(content={"message": "OK"}, status_code=200)
