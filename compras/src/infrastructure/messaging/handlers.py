def handle_product_created(message):
    try:
        print("📩 Mensaje recibido en COMPRAS:", flush=True)
        print(f"🧾 Data: {message.data.decode('utf-8')}", flush=True)
        print(f"🔖 Atributos: {message.attributes}", flush=True)
        message.ack()
    except Exception as e:
        print(f"🚨 Error al procesar mensaje: {e}", flush=True)
        message.nack()
