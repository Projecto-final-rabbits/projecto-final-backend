# Sistema de Gestión CCP -- projecto-final-backend 
 
Este repositorio contiene una aplicación con arquitectura hexagonal basada en microservicios desarrollada con Python y FastAPI, que permite gestionar compras, ventas, clientes y bodegas. Cada microservicio cuenta con su propia base de datos y despliegue independiente.

---

## 🚀 Tecnologías Utilizadas

- **Python 3.11**
- **FastAPI**
- **PostgreSQL**
- **Docker & Docker Compose**
- **SQLAlchemy**
- **Pydantic**
- **Pytest + Coverage**
- **GitHub Actions (CI/CD)**
- **Google Cloud Run**
- **Google Pub/Sub** 

---

## 📁 Estructura de Carpetas

```
.
├── compras/                  # Microservicio de Compras
├── ventas/                   # Microservicio de Ventas
├── clientes/                 # Microservicio de Clientes 
├── bodegas/                  # Microservicio de Bodegas 
├── docker-compose.yml        # Configuración para entorno local
└── .github/                  # Workflows y acciones de CI/CD
```

### Desglose interno del microservicio `compras/`:

```
compras/
├── src/
│   ├── api/
│   │   ├── main.py                      # Punto de entrada FastAPI
│   │   └── routes/                      # Endpoints de la API
│   │       ├── detalles_routes.py
│   │       ├── ordenes_routes.py
│   │       ├── productos_routes.py
│   │       └── proveedores_routes.py
│   ├── application/
│   │   ├── schemas/                     # Schemas de entrada/salida con Pydantic
│   │   │   └── compras.py
│   │   └── services/                    # Lógica de negocio adicional
│   │       └── logic.py
│   ├── config/
│   │   ├── database.py                  # Configuración de SQLAlchemy
│   │   └── .env                         # Variables de entorno (no se versiona)
│   └── infrastructure/
│       ├── adapters/                    # Repositorios con SQLAlchemy
│       │   ├── detalle_repository_sqlalchemy.py
│       │   ├── orden_repository_sqlalchemy.py
│       │   ├── producto_repository_sqlalchemy.py
│       │   └── proveedor_repository_sqlalchemy.py
│       └── db/
│           └── models/                 # Modelos de base de datos
│               └── compra_model.py
├── requirements.txt                    # Dependencias del microservicio
└── tests/                              # Pruebas unitarias con pytest
    ├── api/
    │   ├── test_detalles.py
    │   ├── test_ordenes.py
    │   ├── test_productos.py
    │   └── test_proveedores.py
    ├── db/
    │   └── test_database.py            # Configuración de base de datos SQLite para testing
    └── conftest.py                     # Fixtures y configuración global para pruebas
```

---

## 🧪 Despliegue Local

1. Crear archivo `.env` dentro de cada microservicio (`compras/src/config/.env`, `ventas/src/config/.env`, etc.) con el contenido:

   ```
   DATABASE_URL=postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_basedatos>
   ```

2. Ejecutar el proyecto con Docker Compose:

   ```bash
   docker-compose up --build
   ```

Esto levantará los servicios disponibles en diferentes puertos de tu localhost.

---

## ✅ Tests

Este proyecto incluye pruebas unitarias para todos los endpoints principales.

### ▶️ Ejecutar pruebas en local

1. Asegúrate de tener las dependencias instaladas:
   ```bash
   pip install -r requirements.txt
   ```

2. Corre los tests con:
   ```bash
   pytest --cov=src --cov-fail-under=70
   ```

Esto genera un reporte de cobertura de código. El umbral mínimo está configurado en **70%**.

### 🚀 Pruebas en CI/CD

Todas las pruebas son ejecutadas automáticamente mediante GitHub Actions en cada push o pull request hacia las ramas `develop` o `main`. Si los tests no pasan o el coverage es menor al 70%, el pipeline fallará.

---

## 📚 Documentación Local

Una vez levantado, puedes acceder a Swagger UI de cada microservicio:

- 📘 Compras → [http://localhost:8000/docs#/](http://localhost:8000/docs#/)
- 📘 Ventas → [http://localhost:8001/docs#/](http://localhost:8001/docs#/)
- 📘 Clientes → [http://localhost:8002/docs#/](http://localhost:8002/docs#/)
- 📘 Bodegas → [http://localhost:8003/docs#/](http://localhost:8003/docs#/)

---

## ☁️ Microservicios Desplegados en Cloud Run

- 🌐 Compras → [https://compras-135751842587.us-central1.run.app](https://compras-135751842587.us-central1.run.app)
- 🌐 Ventas → [https://ventas-135751842587.us-central1.run.app](https://ventas-135751842587.us-central1.run.app)
- 🌐 Clientes → `https://clientes-xxxxx.a.run.app` *(pendiente)*
- 🌐 Bodegas → `https://bodegas-xxxxx.a.run.app` *(pendiente)*

---

## 📖 Documentación Swagger en Cloud Run

- 🔎 Compras → [https://compras-135751842587.us-central1.run.app/docs#/](https://compras-135751842587.us-central1.run.app/docs#/)
- 🔎 Ventas → [https://ventas-135751842587.us-central1.run.app/docs#/](https://ventas-135751842587.us-central1.run.app/docs#/)
- 🔎 Clientes → `https://clientes-xxxxx.a.run.app/docs#/`*(pendiente)*
- 🔎 Bodegas → `https://bodegas-xxxxx.a.run.app/docs#/`*(pendiente)*

---

> Este proyecto se encuentra en desarrollo. Pronto se integrará lógica de negocio compleja y mensajería asincrónica usando Pub/Sub.
