from pydantic import BaseModel

class CompraCreate(BaseModel):
    producto: str
    cantidad: int
    proveedor: str

class CompraOut(CompraCreate):
    id: int

    class Config:
        orm_mode = True