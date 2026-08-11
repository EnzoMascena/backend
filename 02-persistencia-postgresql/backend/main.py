"""
Módulo 02 — Persistencia con PostgreSQL
=======================================

La MISMA API de Tareas del Módulo 01, pero con base de datos real.

Módulo 01: los datos vivían en una lista de Python (`tasks: list[dict]`).
           Si reiniciabas el servidor, se perdían.
Módulo 02: los datos viven en PostgreSQL. Sobreviven a reinicios,
           a apagones y a cualquier cosa que le pase al servidor.

REGLA DE ORO DE ESTA CLASE:
    EL CONTRATO DE LA API NO CAMBIA.
    Mismos endpoints, mismos campos, mismo JSON.
    El frontend de la clase 01 funciona sin tocar una línea.

Endpoints (idénticos al Módulo 01):
    GET    /api/tasks         → Listar todas las tareas
    POST   /api/tasks         → Crear una tarea nueva
    PATCH  /api/tasks/{id}    → Toggle completada / no completada
    DELETE /api/tasks/{id}    → Eliminar una tarea

Antes de ejecutar:
    1. Copiá `.env.example` a `.env` y completá DATABASE_URL
       (ver las opciones Docker / Supabase en ese archivo)
    2. Ejecutá `schema.sql` (Docker: psql | Supabase: SQL Editor)
    3. `uv sync` para instalar dependencias

Ejecutar:
    uv run main.py
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field

# ============================================================
# 1. MODELOS DE DATOS (Pydantic)
# ============================================================
# Son IDÉNTICOS al Módulo 01. La API no cambia su forma externa:
# lo que el cliente envía y lo que recibe es exactamente igual.
# Cambió el MOTOR por debajo (lista → PostgreSQL), no el contrato.


class TaskCreate(BaseModel):
    """Modelo para CREAR una tarea. Solo pedimos el título."""

    title: str = Field(..., min_length=1, max_length=200, examples=["Comprar leche"])


class Task(BaseModel):
    """Modelo completo de una tarea (lo que devolvemos al frontend)."""

    id: int
    title: str
    completed: bool
    created_at: str  # String ISO 8601 — mismo formato que el Módulo 01


# ============================================================
# 2. CONEXIÓN A LA BASE DE DATOS
# ============================================================
# ¿De dónde sale la URL? Del archivo .env (o variable de entorno).
# load_dotenv() lee el .env y lo pone disponible para os.getenv().
#
# El default apunta a postgres local con Docker — la demo de clase.
# En el .env de cada alumno va la URL de su proyecto Supabase.

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres",
)

# ¿Qué es un POOL de conexiones?
# Abrir una conexión a la base tarda milisegundos (handshake TCP,
# autenticación, negociación SSL). Si cada request abre UNA conexión
# nueva, desperdiciamos tiempo y satura el servidor de postgres.
#
# El pool mantiene un conjunto de conexiones ABIERTAS y las REUTILIZA:
#   min_size=1 → mantiene al menos 1 conexión viva siempre
#   max_size=10 → como máximo 10 conexiones simultáneas
#
# Analogía: el pool es como un estacionamiento con guardia. Los autos
# (requests) no fabrican su lugar de estacionamiento: el guardia les
# asigna uno ya existente y lo reutiliza cuando se van.
#
# open=False: el pool se abre EXPLÍCITAMENTE en el lifespan (abajo),
# no apenas se importa el módulo.

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10, open=False)


# ============================================================
# 3. APLICACIÓN FASTAPI + LIFESPAN
# ============================================================
# El LIFESPAN define qué pasa cuando el servidor ARRANCA y cuando
# SE APAGA. Es el lugar correcto para abrir/cerrar el pool:
#
#   - Arranque  → pool.open()   → las conexiones están listas
#   - Apagado   → pool.close()  → cerramos limpiamente, sin colgar
#
# ¿Por qué no abrir el pool en cada request? Porque crearlo tiene
# costo. Se crea UNA vez, se reutiliza siempre. Ciclo de vida del
# pool = ciclo de vida del servidor.


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    yield
    pool.close()


app = FastAPI(
    title="Persistencia con PostgreSQL — API de Tareas",
    description="Módulo 02 — La misma API del Módulo 01, ahora con base de datos real.",
    version="0.2.0",
    lifespan=lifespan,
)

# CORS: mismo config que el Módulo 01 (contrato intacto).

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: listar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 4. AYUDANTES DE BASE DE DATOS
# ============================================================


def serialize_task(row: dict) -> dict:
    """
    Convierte una fila de PostgreSQL en el JSON del Módulo 01.

    PostgreSQL guarda created_at como TIMESTAMPTZ y psycopg lo
    devuelve como datetime de Python. El Módulo 01 devolvía un
    string ISO 8601 — lo convertimos EXPLÍCITAMENTE para que el
    contrato de la API no cambie.
    """
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": row["completed"],
        "created_at": row["created_at"].isoformat(),
    }


# ============================================================
# 5. ENDPOINTS — mismos endpoints, ahora con SQL real
# ============================================================
# Patrón que se repite en los 4 endpoints:
#
#   with pool.connection() as conn:
#       conn.row_factory = dict_row   # cada fila llega como DICT
#       with conn.cursor() as cur:
#           cur.execute("... SQL ...", (params,))
#           row = cur.fetchone()
#
#   - pool.connection() → pide una conexión prestada al pool
#   - dict_row → "devolveme cada fila como {"columna": valor}"
#   - conn.cursor() → ejecuta SQL
#   - %s → PLACEHOLDER de parámetros. NUNCA concatenes strings en
#     SQL: es la puerta de entrada a la INYECCIÓN SQL.
#   - al salir del with, la conexión se devuelve al pool (commit
#     automático si no hubo errores)


@app.get("/api/tasks", response_model=list[Task])
def list_tasks():
    """
    SELECT = leer. Trae todas las tareas ordenadas por id.

    fetchall() devuelve TODAS las filas de la consulta.
    """
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, completed, created_at FROM tasks ORDER BY id")
            rows = cur.fetchall()
    return [serialize_task(row) for row in rows]


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(body: TaskCreate):
    """
    INSERT = crear una fila nueva.

    RETURING (postgres) devuelve la fila recién creada — con el id
    y las fechas que la base generó sola. Así no hacemos una segunda
    consulta para saber qué quedó guardado.

    Notá que NO enviamos completed ni created_at:
    la base los genera con sus DEFAULT (FALSE y NOW()).
    """
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title) VALUES (%s) "
                "RETURNING id, title, completed, created_at",
                (body.title.strip(),),
            )
            row = cur.fetchone()
    return serialize_task(row)


@app.patch("/api/tasks/{task_id}", response_model=Task)
def toggle_task(task_id: int):
    """
    UPDATE = modificar una fila existente.

    "SET completed = NOT completed" es SQL puro: si estaba TRUE pasa
    a FALSE y viceversa. El toggle que en el Módulo 01 hacíamos con
    Python ahora lo hace la base, en UNA operación atómica.

    WHERE id = %s → filtra SOLO la tarea pedida. Si no existe,
    UPDATE no toca ninguna fila y fetchone() devuelve None → 404.
    """
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET completed = NOT completed "
                "WHERE id = %s RETURNING id, title, completed, created_at",
                (task_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    return serialize_task(row)


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    """
    DELETE = borrar una fila.

    RETURNING id nos dice CUÁNTAS filas se borraron: si devuelve
    algo, la tarea existía. Si devuelve None, no había nada que
    borrar → 404 (mismo comportamiento que el Módulo 01).
    """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")
    return {"ok": True}


# ============================================================
# 6. HEALTH CHECK — ahora verifica la base de datos
# ============================================================
# En el Módulo 01, el health check contaba los elementos de la
# lista en memoria. Ahora consulta la base de verdad:
#
#   SELECT 1 → la consulta más barata que existe. Si postgres
#   responde, la conexión funciona. Si no responde, el endpoint
#   devuelve error 500 → sabés que el problema es la BBDD.


@app.get("/api/health")
def health_check():
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM tasks")
            count = cur.fetchone()["total"]
    return {
        "status": "Funciona",
        "service": "02-persistencia-postgresql-backend",
        "db": "conectada",
        "tasks_count": count,
    }


# ============================================================
# 7. MAIN — Ejecutar el servidor
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
