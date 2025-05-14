from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.infrastructure.db.models.venta_model import Pedido
from src.infrastructure.db.models.venta_model import DetallePedido
from src.application.schemas.dashboard import SalesSummaryRead, Periodo, TopProductoItem


def obtener_resumen_ventas(
    start_date: date = None,
    end_date: date = None,
    db: Session = None
) -> SalesSummaryRead:
    # Determinar periodo por defecto: mes actual
    today = date.today()
    if start_date is None:
        start_date = today.replace(day=1)
    if end_date is None:
        # fin de mes: primer día del mes siguiente menos un día
        next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_date = next_month - timedelta(days=1)

    # Query base de pedidos en periodo
    pedidos_q = db.query(Pedido).filter(
        Pedido.fecha_envio >= start_date,
        Pedido.fecha_envio <= end_date
    )

    # Total de pedidos
    total_pedidos = pedidos_q.count()

    # Ingresos totales: suma manual de detalle(cantidad * precio_unitario)
    ingresos_q = db.query(
        func.coalesce(func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario), 0.0)
    ).join(Pedido, DetallePedido.pedido_id == Pedido.id).filter(
        Pedido.fecha_envio >= start_date,
        Pedido.fecha_envio <= end_date
    )
    ingresos_totales = ingresos_q.scalar() or 0.0

    # Pedidos por estado
    estados = db.query(
        Pedido.estado,
        func.count(Pedido.id)
    ).filter(
        Pedido.fecha_envio >= start_date,
        Pedido.fecha_envio <= end_date
    ).group_by(Pedido.estado).all()
    pedidos_por_estado = {estado: count for estado, count in estados}

    # Ticket promedio
    ticket_promedio = (ingresos_totales / total_pedidos) if total_pedidos > 0 else 0.0

    # Clientes activos (distinct cliente_id)
    clientes_activos = db.query(func.count(func.distinct(Pedido.cliente_id))).filter(
        Pedido.fecha_envio >= start_date,
        Pedido.fecha_envio <= end_date
    ).scalar() or 0

    # Top productos por ingreso
    productos = db.query(
        DetallePedido.producto_id,
        func.sum(DetallePedido.cantidad).label("cantidad_total"),
        func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario).label("ingreso_generado")
    ).join(Pedido, DetallePedido.pedido_id == Pedido.id).filter(
        Pedido.fecha_envio >= start_date,
        Pedido.fecha_envio <= end_date
    ).group_by(DetallePedido.producto_id)

    top_prods_data = productos.order_by(
        func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario).desc()
    ).limit(5).all()

    top_productos = []
    for prod_id, cantidad, ingreso in top_prods_data:
        # obtener nombre del producto vía relación
        detalle = db.query(DetallePedido).filter(DetallePedido.producto_id == prod_id).first()
        nombre = detalle.producto.nombre if detalle and hasattr(detalle, 'producto') else str(prod_id)
        top_productos.append(TopProductoItem(
            producto_id=prod_id,
            nombre=nombre,
            cantidad_vendida=int(cantidad),
            ingreso_generado=float(ingreso)
        ))

    # Ventas por ciudad (agrupado por direccion_entrega) usando detalle
    ventas_ciudad_q = db.query(
        Pedido.direccion_entrega,
        func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario).label("ingresos_ciudad")
    ).join(DetallePedido, DetallePedido.pedido_id == Pedido.id).filter(
        Pedido.fecha_envio >= start_date,
        Pedido.fecha_envio <= end_date
    ).group_by(Pedido.direccion_entrega).all()
    ventas_por_ciudad = {ciudad: float(total) for ciudad, total in ventas_ciudad_q}

    periodo = Periodo(start_date=start_date, end_date=end_date)

    return SalesSummaryRead(
        periodo=periodo,
        total_pedidos=total_pedidos,
        ingresos_totales=float(ingresos_totales),
        pedidos_por_estado=pedidos_por_estado,
        ticket_promedio=float(ticket_promedio),
        clientes_activos=int(clientes_activos),
        top_productos=top_productos,
        ventas_por_ciudad=ventas_por_ciudad
    )