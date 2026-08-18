"""
Módulo 03 — Arquitectura en Capas
=================================

La MISMA API de Tareas de los módulos 01 y 02, pero organizada en tres
capas. Ahora además el acceso a datos usa un ORM (SQLModel).

    Módulo 01 → main.py con lista en memoria (todo junto)
    Módulo 02 → main.py con SQL crudo de psycopg (todo junto)
    Módulo 03 → capas separadas: Controller → Service → Repository → DB

Qué ganamos:
    - Cada archivo tiene UNA responsabilidad
    - Se puede testear cada capa por separado
    - Si cambia la base o el ORM, solo cambia el repository
    - El contrato de la API se mantiene: mismo JSON, mismos campos

Este archivo es SOLO el entrypoint: crea la app, registra los routers
y maneja el arranque. No tiene lógica de negocio ni SQL.

Antes de ejecutar:
    1. Copiá `.env.example` a `.env` y completá DATABASE_URL
    2. `uv sync` para instalar dependencias
    (la tabla se crea sola al arrancar — ya no hace falta schema.sql)

Ejecutar:
    uv run -m app.main
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import health_controller, task_controller
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Al arrancar: crea las tablas (si no existen).
    Al apagar: nada que liberar (la Session se cierra sola por request).

    En el Módulo 02 abríamos/cerrábamos un pool acá. Con el ORM, la
    gestión de conexiones es por request (get_session), no global.
    """
    create_db_and_tables()
    yield


app = FastAPI(
    title="Arquitectura en Capas — API de Tareas",
    description=(
        "Módulo 03 — La misma API del Módulo 02, organizada en "
        "Controller → Service → Repository, con SQLModel como ORM."
    ),
    version="0.3.0",
    lifespan=lifespan,
)

# CORS: mismo config que los módulos anteriores.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: listar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos los routers. Cada controller expone sus propios endpoints.
app.include_router(task_controller.router)
app.include_router(health_controller.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
