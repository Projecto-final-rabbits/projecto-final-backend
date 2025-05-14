from datetime import date
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class Periodo(BaseModel):
    start_date: date = Field(..., description="Fecha de inicio del periodo")
    end_date: date = Field(..., description="Fecha de fin del periodo")


class TopProductoItem(BaseModel):
    producto_id: UUID
    nombre: str
    cantidad_vendida: int
    ingreso_generado: float


class SalesSummaryRead(BaseModel):
    periodo: Periodo
    total_pedidos: int = Field(..., description="Cantidad total de pedidos en el periodo")
    ingresos_totales: float = Field(..., description="Suma de ingresos de todos los pedidos en el periodo")
    pedidos_por_estado: Dict[str, int] = Field(..., description="Conteo de pedidos agrupados por estado")
    ticket_promedio: float = Field(..., description="Ingreso promedio por pedido en el periodo")
    clientes_activos: int = Field(..., description="Número de clientes distintos que realizaron pedidos")
    top_productos: List[TopProductoItem] = Field(..., description="Lista de los principales productos por ingreso")
    ventas_por_ciudad: Dict[str, float] = Field(..., description="Ingresos totales agrupados por ciudad de entrega")

    class Config:
        orm_mode = True
