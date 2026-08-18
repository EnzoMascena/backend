"""
Capa de infraestructura — la conexión a la base de datos.

Acá vive TODO lo que toca PostgreSQL: la URL de conexión, el motor
(engine) de SQLAlchemy y la creación de tablas. Ninguna otra capa
importa al driver directamente: solo piden una sesión.

En el Módulo 02 esto era un `pool` de psycopg con SQL crudo. Ahora el
ORM (SQLModel) maneja las conexiones por nosotros: pedimos una `Session`
y él se encarga del resto.
"""

import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

# La URL sale del .env (o variable de entorno). Mismo patrón que el
# Módulo 02. El default apunta a postgres local con Docker (la demo).
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres",
)

# El ENGINE es el "motor" que sabe hablar con la base. Guarda la URL,
# gestiona las conexiones y ejecuta el SQL. Se crea UNA sola vez.
engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    """
    Crea las tablas a partir de los modelos ORM.

    Antes (Módulo 02) ejecutábamos `schema.sql` a mano. Ahora el ORM
    lee los modelos (las clases con `table=True`) y genera el `CREATE
    TABLE` por nosotros. Es idempotente: si la tabla ya existe, no la
    toca (por eso podés reutilizar la base del Módulo 02 sin romperla).
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Proporciona una SESIÓN por cada request (generador para FastAPI).

    La sesión es la "ventanilla" del ORM: con ella leés y escribís en
    la base. Se abre al empezar el request y se cierra al terminar
    (el `with` hace commit/rollback automático según haya error o no).
    """
    with Session(engine) as session:
        yield session
