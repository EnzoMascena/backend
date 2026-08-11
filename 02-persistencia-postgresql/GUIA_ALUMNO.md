# 📋 Guía del Alumno — Persistencia con PostgreSQL

> **Materia**: Desarrollo de Software — Módulo 02
> **Duración**: 90 minutos
> **Taller guiado**: sí
>
> **IMPORTANTE**: Vas a migrar la API del Módulo 01 de la memoria a una
> base de datos real. Archivo por archivo, desde cero. Abrí esta guía en
> tu navegador y copiá el código de cada archivo en tu editor.
> No clonamos nada — todo lo escribís vos.

---

## Cómo usar esta guía

1. Cada archivo tiene su bloque de código **completo y listo para copiar**
2. Respetá el **orden de creación** (las partes dependen entre sí)
3. Después de cada archivo, seguí las **instrucciones de verificación** antes de avanzar
4. Si algo falla: **leé el error**, preguntá al docente, NO sigas adelante
5. Dos caminos conviven en esta clase: **Docker** (lo demuestra el docente) y **Supabase** (lo usás vos). Ambos son **PostgreSQL** — la única diferencia es la URL de conexión.

---

## Plan de la clase (90 minutos)

| Fase | Tema | Tiempo |
|------|------|--------|
| Fase 1 | El hook: los datos mueren al reiniciar | 5' |
| Fase 2 | Mini intro: el docente levanta PostgreSQL con Docker | 15' |
| Fase 3 | SQL en 10 minutos | 10' |
| Fase 4 | La conexión | 10' |
| Fase 5 | Migrar la API | 35' |
| Fase 6 | Cierre: el frontend no se entera de nada + Postman | 15' |

---

## PARTE A — El hook: los datos mueren al reiniciar (5 min)

### A.1 Qué quedó del Módulo 01

En la clase anterior construiste una API de tareas con FastAPI. ¿Te acordás
de cómo guardaba los datos? Así:

```python
tasks: list[dict] = []
next_id: int = 1
```

Una **lista en memoria RAM**. Funciona perfecto… mientras el servidor está
encendido. El momento incómodo llega cuando lo apagás.

### A.2 La demostración del docente

El docente va a hacer esto en vivo, con la app del Módulo 01:

1. Levanta el backend (`uv run main.py`)
2. Crea una tarea con Postman o Swagger: *"Comprar leche"*
3. Lista las tareas → aparece en la lista ✅
4. **Apaga el servidor** (`CTRL+C`)
5. **Lo vuelve a prender**
6. Lista las tareas → la lista está **vacía** ❌

> 🔥 **¿Qué pasó?** La tarea *"Comprar leche"* vivía en la RAM del proceso
> Python. Cuando el proceso murió, la memoria se liberó y el dato se fue con
> ella. No lo borró nadie: simplemente nunca existió en un lugar permanente.

### A.3 El problema en serio

Esto NO es una curiosidad de clase. Es el problema central que resuelven las
**bases de datos**: los datos tienen que sobrevivir al proceso que los creó.

Pensalo con ejemplos del mundo real:

- Una app de banco: tu saldo no puede depender de que el servidor no se reinicie
- Un e-commerce: tu carrito no puede desaparecer cada vez que se cae un servidor
- Una red social: tus posts tienen que seguir ahí años después de que el dev que los programó se fue de la empresa

> 🧠 **Concepto clave de hoy**: la **persistencia**. El dato vive en un lugar
> estable (el disco de un servidor de base de datos), separado del proceso
> que lo atiende. El proceso puede morir mil veces; el dato queda.

### A.4 El plan de la clase y la REGLA DE ORO

Hoy no construimos una API nueva. **Migramos** la del Módulo 01:

| | Módulo 01 | Módulo 02 |
|---|---|---|
| Almacenamiento | `tasks: list[dict]` (memoria) | Tabla `tasks` en PostgreSQL |
| `created_at` | `datetime.now()` en Python | `NOW()` en la base |
| `id` | `next_id += 1` en Python | `IDENTITY` en la base |
| Los datos sobreviven a un reinicio | ❌ No | ✅ Sí |
| El JSON que devuelve la API | `id, title, completed, created_at` | **idéntico** |
| Los endpoints | 4 + health | **idénticos** |
| El frontend de la clase 01 | JavaScript | **se reutiliza sin tocar una línea** |

**REGLA DE ORO DE ESTA CLASE:**

> 🥇 **EL CONTRATO DE LA API NO CAMBIA.**
> Mismos endpoints, mismos campos, mismo JSON.
> El frontend de la clase 01 funciona sin tocar una línea.

Todo lo que va a pasar hoy se resume en una frase: **cambiamos el motor por
debajo del capó, sin que el que maneja se dé cuenta.**

---

## PARTE B — La base de datos: dos caminos, un solo PostgreSQL (15 min)

### B.1 ¿Qué es una base de datos relacional? (30 segundos de teoría)

Una base relacional guarda los datos en **tablas** (filas y columnas). Cada
tabla es un "molde" de una entidad: acá vamos a tener una tabla `tasks` donde
cada **fila** es una tarea y cada **columna** un atributo (`id`, `title`,
`completed`, `created_at`).

PostgreSQL es un motor de base de datos relacional. Es gratis, open source,
super robusto, y es el que usan muchísimas empresas en producción. Hoy lo vas
a tocar por primera vez en serio.

### B.2 Demostración del docente: Docker en 3 comandos

> 👨‍🏫 **ESTA SECCIÓN ES DEMO.** El docente la hace frente a la clase.
> Vos **NO tipeás estos comandos** — tu camino es Supabase (sección B.3).

Docker permite levantar un PostgreSQL entero en una línea, sin instalarlo en
la máquina. El docente va a hacer esto:

```bash
# Descarga la imagen de PostgreSQL 16 y la corre en un contenedor
docker run --name pg-clase02 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5432:5432 \
  -d postgres:16-alpine

# Verificar que el contenedor está corriendo
docker ps

# Entrar a la consola SQL de PostgreSQL
docker exec -it pg-clase02 psql -U postgres
```

Ojo lo que acabás de ver: un **servidor de base de datos completo** corriendo
con un comando. No instaló nada en su sistema, no configuró nada. Esa imagen
`postgres:16-alpine` es liviana y sirve para la demo. Más adelante, en la
materia, vas a profundizar en Docker.

> 🧠 **Anotá esto** (vale oro): el mismo PostgreSQL que el docente levantó con
> Docker en 30 segundos es el que vos vas a usar hoy, solo que **en la nube**
> (Supabase). "Cualquier PostgreSQL sirve, solo cambia la URL."

### B.3 Alumno: crear tu proyecto en Supabase (tu base de datos, gratis)

Mientras el docente hace la demo, vos creás tu base en la nube. **Cero
instalación** — todo desde el navegador.

1. Entrá a **https://supabase.com**
2. Creá una cuenta (podés usar tu GitHub)
3. Click en **New project**
4. Completá:
   - **Name**: `desa-soft-2026`
   - **Database Password**: una contraseña que inventes y **guardes** (la vas a necesitar)
   - **Region**: la más cercana que encuentres (no importa mucho para esta clase)
   - Plan: **Free** (gratis, no te pide tarjeta)
5. Click en **Create new project** y esperá el **provisioning** (1-2 minutos)
6. Cuando el proyecto esté listo, abrí la pestaña **SQL Editor** — es tu
   consola SQL en el navegador. Vas a pegar ahí el `schema.sql` en la Fase 3.

> ⏳ **Mientras Supabase provisiona** (tarda un par de minutos): aprovechá y
> hacé la sección B.4 acá abajo, que no depende de la base. No perdés tiempo.

### B.4 El ticket de acceso: la connection string

Una **connection string** (o *string de conexión*) es "la dirección completa"
de tu base de datos. Es el dato que más vas a usar hoy — guardalo, es tu
**ticket de acceso**.

En Supabase:

1. Entrá a **Settings** (engranaje abajo a la izquierda) → **Database**
2. Buscá la sección **Connection string**
3. Copiá la URL del **POOLER → Transaction** (¡ojo, es el POOLER, no la Direct!):
   - Es el que funciona sobre **IPv4** → más confiable en redes de universidad (la conexión directa pide IPv6 en algunos casos)
   - Fijate que el puerto es **6543**
4. Pegala en un editor de texto aparte. Va a tener esta forma:

```
postgresql://postgres.TU_PROJECT_REF:TU_PASSWORD@aws-0-TU_REGION.pooler.supabase.com:6543/postgres
```

> ⚠️ **Atención**: tu URL real ya viene con tu project ref, tu región y tu
> contraseña adentro. La de arriba es solo la *forma*. No compartas tu URL:
> es la puerta de entrada a tu base de datos.

### B.5 Crear la estructura de directorios y el primer archivo (2 min)

Abrí una terminal y creá la carpeta del Módulo 02:

```bash
mkdir -p 02-persistencia-postgresql/backend
```

Ahora, **el primer archivo de la clase**: `backend/pyproject.toml`.

> **Editor**: creá el archivo `pyproject.toml` dentro de
> `02-persistencia-postgresql/backend/` con este contenido.

```toml
[project]
name = "02-persistencia-postgresql-backend"
version = "0.1.0"
description = "API de Tareas — Persistencia con PostgreSQL"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "psycopg[binary]>=3.2.0",
    "psycopg-pool>=3.2.0",
    "python-dotenv>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
```

**Qué es**: el manifiesto del proyecto. Comparalo con el del Módulo 01 — ¿ves
las tres dependencias nuevas?

- `psycopg[binary]` — el "conductor" de Python para PostgreSQL. Es la librería que ejecuta el SQL.
- `psycopg-pool` — el manejo del **pool de conexiones** (lo vemos en la Fase 4).
- `python-dotenv` — lee el archivo `.env` con la configuración.

> 👨‍🏫 **Anotá esto**: `psycopg` es el cliente PostgreSQL más usado de Python.
> Cuando en una empresa te digan "conectate a la base", la mayoría de las veces
> es esto: `psycopg`.

---

## PARTE C — SQL en 10 minutos (10 min)

### C.1 La idea

Ahora vas a definir **la estructura** de tus datos. En el Módulo 01 la
estructura estaba en el código Python (el dict con `id`, `title`, `completed`,
`created_at`). Ahora la estructura va a vivir en la base, en un lenguaje
llamado **SQL** (Structured Query Language).

Los archivos SQL que definen la estructura se llaman **esquemas** (schema).

### C.2 Crear `backend/schema.sql`

> **Editor**: creá el archivo `schema.sql` dentro de `backend/` con este
> contenido.

```sql
-- ============================================================
-- Esquema de la base de datos — Módulo 02: Persistencia
-- ============================================================
-- Este archivo define la ESTRUCTURA de los datos (el "molde").
-- PostgreSQL lo ejecuta UNA sola vez por proyecto.
--
-- ¿Por qué "IF NOT EXISTS"?
-- Para poder ejecutarlo varias veces sin que rompa.
-- Así es IDEMPOTENTE: si la tabla ya existe, no hace nada.
--
-- ¿Cómo se ejecuta?
--   Docker (demo):  docker exec -i pg-clase02 psql -U postgres < schema.sql
--   Supabase:       SQL Editor del dashboard → pegar el contenido → Run
-- ============================================================

CREATE TABLE IF NOT EXISTS tasks (
    -- id: número único por fila. IDENTITY = PostgreSQL elige el
    -- próximo número automáticamente (1, 2, 3...). Es la clave
    -- primaria (PRIMARY KEY): identifica a la tarea sin ambigüedad.
    id          INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- title: el texto de la tarea. NOT NULL = no puede faltar.
    -- TEXT permite cualquier longitud (la validación de 1..200
    -- caracteres la hace Pydantic en la API, como en el Módulo 01).
    title       TEXT        NOT NULL,

    -- completed: estado de la tarea. DEFAULT FALSE = al crear,
    -- una tarea arranca sin completar. No hace falta decir
    -- "completed: false" en el INSERT: la base lo decide sola.
    completed   BOOLEAN     NOT NULL DEFAULT FALSE,

    -- created_at: cuándo se creó. TIMESTAMPTZ = timestamp CON zona
    -- horaria (la "T" de postgres + "Z" de UTC).
    -- DEFAULT NOW() = la base pone la fecha, no el código Python.
    -- ¿Quién genera el dato? LA FUENTE DE VERDAD: la base.
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Traducción línea por línea** (vale la pena, son 10 segundos):

- `CREATE TABLE IF NOT EXISTS tasks` — creá una tabla llamada `tasks`; si ya existe, no rompas.
- `id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` — el **id lo elige la base** (1, 2, 3…). Acá murió el `next_id += 1` del Módulo 01.
- `title TEXT NOT NULL` — texto, obligatorio. La validación de largo (1–200) la sigue haciendo Pydantic en la API, igual que antes.
- `completed BOOLEAN NOT NULL DEFAULT FALSE` — arranca en `false` solo. No hace falta mandarlo en el INSERT.
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()` — **la fecha la pone la base**, con zona horaria. Acá murió el `datetime.now(timezone.utc)` de Python.

> 🧠 **La decisión de diseño más importante**: quién genera cada dato.
> En el Módulo 01 el *código* generaba el `id` y la fecha. Ahora la **base**
> los genera sola. La base es **la fuente de verdad** — el código solo le pide
> cosas. Si mañana cambia el lenguaje de programación, los datos quedan intactos.

### C.3 Ejecutar el esquema

Según tu camino:

**Camino Docker (si estás siguiendo la demo del docente):**

```bash
docker exec -i pg-clase02 psql -U postgres < schema.sql
```

**Camino Supabase (tu caso si usás la nube):**

1. Abrí el **SQL Editor** de tu proyecto
2. Pegá todo el contenido de `schema.sql`
3. Click en **Run** → te tiene que decir `Success`

### C.4 Los 4 comandos mágicos de SQL

SQL tiene 4 operaciones básicas, que coinciden con las 4 operaciones de tu API.
Se conocen como **CRUD**: **C**reate, **R**ead, **U**pdate, **D**elete.

Abrí tu consola SQL (Docker: `docker exec -it pg-clase02 psql -U postgres` |
Supabase: SQL Editor) y ejecutá estos ejemplos sobre la tabla `tasks`:

**1. INSERT — crear una fila**

```sql
INSERT INTO tasks (title) VALUES ('Practicar SQL');
```

Fijate que **no** mandamos `id`, ni `completed`, ni `created_at`: la base los
genera sola (IDENTITY, DEFAULT FALSE, DEFAULT NOW()).

**2. SELECT — leer**

```sql
SELECT id, title, completed, created_at FROM tasks;
```

La consola te muestra la fila recién creada con todos los datos generados.

**3. UPDATE — modificar**

```sql
UPDATE tasks SET completed = TRUE WHERE id = 1;
```

> 🧠 **`WHERE` es el filtro** — sin `WHERE`, el UPDATE toca TODAS las filas.
> Olvidar el `WHERE` es el clásico error que borra medio sistema de producción.
> Repetilo: **sin `WHERE` no hay filtro, y sin filtro se actualiza todo.**

**4. DELETE — borrar**

```sql
DELETE FROM tasks WHERE id = 1;
```

> ⚠️ **Mismo cuidado que arriba**: `DELETE FROM tasks;` sin `WHERE` vacía la
> tabla entera. En la nube (Supabase) hay protecciones, pero en producción el
> `WHERE` es tu vida.

### C.5 Verificar el esquema

Verificá que la estructura quedó bien con:

```sql
SELECT * FROM tasks;
```

Si ya probaste los comandos de arriba, puede estar vacía o tener filas — no
importa. Lo importante es que **no dé error** y te muestre las columnas:
`id | title | completed | created_at`.

---

### ✅ CHECKPOINT 1 — La base está arriba y conectada (parte 1: la base)

Pará un segundo y verificá qué tenés:

- ✅ ¿Creaste el proyecto en Supabase y copiaste la connection string del **pooler** (puerto 6543)?
- ✅ ¿Tenés el `pyproject.toml` creado?
- ✅ ¿Ejecutaste el `schema.sql` y la tabla `tasks` existe? (probá `SELECT * FROM tasks;`)

**¿Algo falla?** Preguntá al docente AHORA. Si la base no está lista, el resto
de la clase no tiene sentido. Dale, ponete las pilas.

---

## PARTE D — La conexión (10 min)

### D.1 Anatomía de la connection string

Mirá la URL que copiaste de Supabase. Todas las connection strings de
PostgreSQL tienen la misma forma, con **5 partes**:

```
postgresql://  USUARIO  :  CONTRASEÑA  @  HOST  :  PUERTO  /  BDD
   ^protocolo    ^usuario     ^clave        ^dónde      ^puerta  ^nombre
```

| Parte | En tu URL de Supabase | Qué es |
|-------|----------------------|--------|
| `postgresql://` | `postgresql://` | El protocolo: qué tipo de base es |
| usuario | `postgres.TU_PROJECT_REF` | El usuario de la base |
| contraseña | `TU_PASSWORD` | Tu clave (la que inventaste al crear el proyecto) |
| host | `aws-0-TU_REGION.pooler.supabase.com` | ¿Dónde vive la base? Un servidor de Supabase en la nube |
| puerto | `6543` | La "puerta" de entrada. **6543 = pooler** (IPv4) |
| base | `postgres` | El nombre de la base de datos |

> 🧠 **La misma URL con otro puerto = otra cosa**. La conexión "direct" de
> Supabase usa el puerto **5432** pero pide IPv6 en muchos casos, y las redes
> de universidad con IPv4 a secas no lo resuelven. El **pooler** (6543)
> funciona sobre IPv4 → es el que usamos hoy. Este tipo de detalles es lo que
> separa a un dev que lee la doc de uno que solo copia.

### D.2 ¿Por qué un `.env`? El secreto fuera del código

La URL de conexión tiene tu **contraseña**. No puede vivir en el código fuente
(main.py se comparte, se commitea, se sube a GitHub…). La solución estándar:
un archivo **`.env`** (de *environment*) que **no se sube al repo**, y que el
código lee al arrancar.

- `load_dotenv()` — lee el `.env` y deja las variables disponibles
- `os.getenv("DATABASE_URL")` — trae el valor de esa variable

Separás así la **configuración** (varía por máquina) del **código** (es igual
para todos).

### D.3 Crear `backend/.env`

> **Editor**: creá el archivo `.env` dentro de `backend/` con este contenido.
> Luego completá la OPCIÓN 2 con TU connection string.

```env
# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================
# Copiá este archivo como `.env` y completá la URL según tu caso.
#
# La URL de conexión (connection string) es "la dirección completa"
# de la base de datos. Tiene 5 partes:
#
#   postgresql://  USUARIO  :  CONTRASEÑA  @  HOST  :  PUERTO  /  BDD
#   ^protocolo    ^usuario     ^clave        ^dónde      ^puerta  ^nombre
#
# ─────────────────────────────────────────────────────────────
# OPCIÓN 1 — PostgreSQL local con DOCKER (demo del docente)
# ─────────────────────────────────────────────────────────────
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres

# ─────────────────────────────────────────────────────────────
# OPCIÓN 2 — Supabase free tier (alumnos)
# ─────────────────────────────────────────────────────────────
# 1. Creá un proyecto en https://supabase.com (plan Free)
# 2. Settings → Database → "Connection string"
# 3. Copiá la URL del POOLER (Transaction, puerto 6543):
#    - Es el que funciona sobre IPv4 → más confiable en redes
#      de universidad (la conexión directa pide IPv6 en algunos casos)
#    - En la clase decimos "cualquier PostgreSQL sirve, solo cambia
#      la URL" — acá está la prueba
#
DATABASE_URL=postgresql://postgres.TU_PROJECT_REF:TU_PASSWORD@aws-0-TU_REGION.pooler.supabase.com:6543/postgres

# ─────────────────────────────────────────────────────────────
# OPCIÓN 3 — Tu propio PostgreSQL local instalado en la máquina
# ─────────────────────────────────────────────────────────────
# DATABASE_URL=postgresql://usuario:password@localhost:5432/mi_bdd
```

Reemplazá `postgresql://postgres.TU_PROJECT_REF:TU_PASSWORD@aws-0-TU_REGION.pooler.supabase.com:6543/postgres` por **tu** connection string completa (el paso B.4).

> ⚠️ **Dos detalles importantes**:
> - El `.env` empieza con punto — es un archivo oculto (y el `.gitignore` del proyecto ya lo excluye del repo). Nunca lo subas a GitHub.
> - Fijate que solo la **OPCIÓN 2** está "descomentada" (sin `#`). Las otras quedan de referencia.

### D.4 ¿Qué es un POOL de conexiones? (la analogía del estacionamiento)

Cada vez que el backend necesita hablar con la base, tiene que **abrir una
conexión**: handshake TCP, autenticación, negociación SSL… eso tarda
**milisegundos**. Si cada request abre una conexión nueva y la cierra, gastás
tiempo y saturás al servidor de PostgreSQL.

La solución: un **pool**. Un conjunto de conexiones que quedan **abiertas** y
se **reutilizan**.

> 🅿️ **Analogía**: el pool es un estacionamiento con guardia. Los autos
> (los requests) no fabrican su lugar de estacionamiento: el guardia les
> asigna uno que ya existe y lo reutiliza cuando se van. Configurás cuántos
> lugares (conexiones) hay: acá `min_size=1` (siempre hay al menos uno vivo)
> y `max_size=10` (nunca más de 10 a la vez).

### D.5 `psycopg`: el conductor

`psycopg` es el **conductor** entre Python y PostgreSQL. Tu código Python no
habla "sql" nativamente: le pasa la consulta a psycopg, psycopg la lleva a la
base, trae las filas y te las entrega como objetos de Python. Todo lo que
escribimos en la Fase 5 se apoya en esto.

---

## PARTE E — Migrar la API (35 min)

### E.1 Crear `backend/main.py`

> **Editor**: creá el archivo `main.py` dentro de `backend/` con este
> contenido.
> **Son ~300 líneas. Copialo completo, no saltees ninguna parte.**
> Comparalo mentalmente con el del Módulo 01 — vas a ver que el contrato es idéntico.

```python
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
```

### E.2 Las piezas clave de lo que acabás de escribir

Este es el corazón de la clase. Cinco patrones que vas a usar en TODA tu
carrera como backend. No los saltees — leelos dos veces si hace falta.

#### E.2.1 `%s` — los placeholders y la inyección SQL

Mirá el INSERT:

```python
cur.execute(
    "INSERT INTO tasks (title) VALUES (%s) ",
    (body.title.strip(),),
)
```

El `%s` es un **placeholder**: un hueco en la consulta que psycopg llena con
el valor del segundo argumento. **NUNCA, JAMÁS, en serio**, hagas esto:

```python
# ❌ NUNCA — concatenar strings en SQL
cur.execute(f"INSERT INTO tasks (title) VALUES ('{body.title}')")
```

¿Por qué? Porque si `body.title` es una cadena maliciosa, el atacante puede
"escaparse" de las comillas y ejecutar SQL que NO le pediste. Eso se llama
**inyección SQL** y es una de las vulnerabilidades más explotadas de la
historia. Con `%s`, psycopg escapa el valor: llega como **dato**, jamás como
**código SQL**. No es una preferencia estética: es una barrera de seguridad.
Vas a comprobarlo en carne propia en el ejercicio 🔴 7.

#### E.2.2 `RETURNING` — que la base te devuelva lo que hizo

```sql
INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, completed, created_at
```

En el Módulo 01, vos calculabas el `id` y la fecha en Python y armabas la
tarea a mano. Ahora **la base** genera `id`, `completed` y `created_at` — y
`RETURNING` te devuelve la fila recién creada, completa. Una sola consulta, sin
un segundo `SELECT` para preguntar "¿qué quedó guardado?". Postgres te ahorra
un round-trip y vos te quedás tranquilo: lo que devolvés es EXACTAMENTE lo que
quedó en la base.

#### E.2.3 `completed = NOT completed` — el toggle lo hace la base

```sql
UPDATE tasks SET completed = NOT completed WHERE id = %s RETURNING ...
```

En el Módulo 01, el toggle era Python puro:

```python
task["completed"] = not task["completed"]
```

Ahora lo hace SQL: `NOT completed` niega el valor actual (TRUE↔FALSE), y como
es **una sola operación atómica**, no hay forma de que quede un estado
intermedio. La lógica de negocio que antes vivía en tu código ahora vive en
la consulta — y funciona igual, porque el resultado es el mismo.

#### E.2.4 `dict_row` — cada fila como diccionario

```python
conn.row_factory = dict_row
```

PostgreSQL te devuelve filas; psycopg tiene que convertirlas a algo usable en
Python. Con `dict_row`, cada fila llega como `{"id": 1, "title": "Comprar leche", ...}`
— accedés por nombre de columna: `row["id"]`, `row["title"]`. Sin esto,
tendrías tuplas posicionales (`row[0]`, `row[1]`) y el código se vuelve
frágil: si mañana alguien agrega una columna en el medio, todo se rompe.
Con nombres, el código se lee solo.

#### E.2.5 `serialize_task` — el puente de formato

```python
def serialize_task(row: dict) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": row["completed"],
        "created_at": row["created_at"].isoformat(),
    }
```

Postgres guarda `created_at` como `TIMESTAMPTZ` y psycopg te lo entrega como
un objeto `datetime` de Python. Pero el frontend del Módulo 01 espera un
**string ISO 8601** (igual que devolvía `datetime.now(timezone.utc).isoformat()`).
`.isoformat()` convierte el datetime al formato exacto. Este helper es el
"traductor" que mantiene el contrato intacto — el frontend no tiene idea de
que antes había un datetime de Python y ahora un TIMESTAMPTZ de Postgres.

#### E.2.6 `lifespan` — el ciclo de vida del servidor

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()
    yield
    pool.close()
```

FastAPI necesita un lugar para abrir el pool cuando el servidor arranca y
cerrarlo cuando se apaga. Eso es el `lifespan`: el código **antes** del
`yield` corre al arranque (`pool.open()` — las conexiones quedan listas), y
el **después** corre al apagado (`pool.close()` — cierre limpio, sin colgar).
El pool no se crea por request: se crea **una vez** y vive tanto como el
servidor. Por eso el `ConnectionPool` se define con `open=False` — la apertura
explícita se delega al lifespan, no al import del módulo.

> 🧠 **Resumen del patrón completo** (memorizalo): *pedir conexión al pool →
> decirle a psycopg que las filas vengan como dict → ejecutar SQL con
> placeholders `%s` → serializar al formato del contrato → devolver el JSON
> de siempre.* Los 4 endpoints siguen exactamente ese patrón.

### E.3 Instalar dependencias

```bash
cd 02-persistencia-postgresql/backend
uv sync
```

Debés ver que se instalan `fastapi`, `uvicorn`, `psycopg`, `psycopg-pool` y
`python-dotenv` (y sus dependencias). Si falla, revisá que el `pyproject.toml`
no tenga errores de sintaxis.

### E.4 Ejecutar el servidor

```bash
uv run main.py
```

Debés ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

> ⚠️ **NO cierres esta terminal** — el servidor tiene que quedar corriendo.
>
> 🔍 **Ojo con el lifespan**: si el pool NO pudo conectarse (URL mal copiada,
> Supabase todavía provisionando), el arranque puede fallar o colgarse. Si
> ves un error de conexión, revisá el `.env` y la URL del pooler.

### E.5 Probar con curl (nueva terminal)

```bash
# Health check — ahora verifica la base de datos
curl http://localhost:8000/api/health

# Listar (debería estar vacío o con las filas que insertaste a mano)
curl http://localhost:8000/api/tasks

# Crear una tarea
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender PostgreSQL"}'

# Listar de nuevo (debería tener 1 tarea, con id y fecha generados por la base)
curl http://localhost:8000/api/tasks

# Marcar como completada (ID 1)
curl -X PATCH http://localhost:8000/api/tasks/1

# Eliminar (ID 1)
curl -X DELETE http://localhost:8000/api/tasks/1

# Health check otra vez — tasks_count cambió
curl http://localhost:8000/api/health
```

> 🧠 **Detalle fino**: en la respuesta del POST fijate el `created_at` — el
> formato es idéntico al del Módulo 01, pero el dato lo generó **PostgreSQL**,
> no Python. Y el `id` lo eligió la base con IDENTITY. Sospectá: la lista
> `tasks` y `next_id` ya no existen en ningún lado — ¿de dónde salen esos
> números? De la tabla. La base manda.

---

### ✅ CHECKPOINT 1 — La base está arriba y conectada (parte 2: la API)

Abrí en tu navegador: **http://localhost:8000/docs**

Debés ver Swagger con los mismos 4 endpoints de siempre. Después entrá a
**http://localhost:8000/api/health** — debe responder:

```json
{
  "status": "Funciona",
  "service": "02-persistencia-postgresql-backend",
  "db": "conectada",
  "tasks_count": 0
}
```

La clave es **`"db": "conectada"`**. Si la ves, el backend está hablando con
tu PostgreSQL (Supabase o Docker) de verdad. Estás a un paso del milagro.

**¿No aparece?** Revisá:
- ¿La terminal de `uv run main.py` muestra un error de conexión? → pegale el mensaje al docente
- ¿Copiaste bien la connection string del **pooler** (puerto 6543) en el `.env`?
- ¿Ejecutaste el `schema.sql` y la tabla `tasks` existe?

---

## PARTE F — Cierre: el frontend no se entera de nada (15 min)

### F.1 La prueba de fuego: la persistencia (el momento de la clase)

Este es el momento que esperamos toda la clase. Hacelo paso a paso:

1. Creá 2 o 3 tareas desde Swagger o curl (por ejemplo: *"Comprar leche"*, *"Estudiar SQL"*)
2. Listalas → están ahí
3. **Matá el servidor**: `CTRL+C` en la terminal del backend
4. Volvé a levantarlo: `uv run main.py`
5. Listá las tareas → **SIGUEN AHÍ**

> 🔥 **Ahí lo tenés**: en la Fase 1, reiniciar el servidor borraba todo. Ahora
> los datos sobreviven. El proceso Python murió y revivió; la base nunca se
> enteró. Eso es **persistencia** — el dato ya no depende del proceso que lo
> atiende. Comparalo con la demo del inicio de la clase y llenate.

### F.2 El clímax pedagógico: reutilizar el frontend del Módulo 01

Ahora la parte que cierra el círculo. El frontend React de la clase pasada no
sabe NADA de PostgreSQL. Sigue hablando HTTP con los mismos endpoints y el
mismo JSON. Reutilizalo tal cual:

```bash
cd ../01-mi-primera-app/frontend
pnpm dev
```

Debés ver:

```
  VITE v6.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

> El proxy de Vite ya apunta a `localhost:8000` (lo configuraste en la clase 1)
> — el frontend sigue hablando con la misma URL de siempre.

Abrí **http://localhost:5173** y usá la app normal:

1. Agregá una tarea → aparece
2. Marcala como completada → se tacha
3. Eliminala → desaparece
4. **Reiniciá el backend y recargá la página** → las tareas siguen ahí

> 🧠 **El momento de reflexión**: el frontend NO CAMBIÓ UNA LÍNEA. Mismo
> JavaScript, mismo fetch, mismas URLs. Por debajo cambió el motor completo
> (memoria → base de datos en la nube) y el frontend no se enteró. Eso es lo
> que compra el **contrato de la API**: cuando respetás el contrato, podés
> cambiar TODO el interior sin tocar a los consumidores. Esa es la base de
> las arquitecturas que escalan.

### F.3 Probar con Postman / Bruno

1. Abrí Postman (o Bruno)
2. Creá una Collection llamada "Persistencia con PostgreSQL"
3. Agregá los 5 requests:

| Nombre | Método | URL | Body |
|--------|--------|-----|------|
| Health | `GET` | `http://localhost:8000/api/health` | — |
| Listar tareas | `GET` | `http://localhost:8000/api/tasks` | — |
| Crear tarea | `POST` | `http://localhost:8000/api/tasks` | `{"title": "Mi tarea"}` |
| Toggle tarea | `PATCH` | `http://localhost:8000/api/tasks/1` | — |
| Eliminar tarea | `DELETE` | `http://localhost:8000/api/tasks/1` | — |

> 🧠 **La colección es exactamente la misma que la del Módulo 01.** Los
> requests no cambiaron — porque la API no cambió. Si conservás la collection
> anterior, funcionó sin tocar nada.

---

### ✅ CHECKPOINT 2 — La persistencia está probada

- ✅ ¿Creaste tareas, reiniciaste el servidor y **siguen estando**?
- ✅ ¿El frontend del Módulo 01 funciona **sin cambios** contra el backend nuevo?
- ✅ ¿El health check dice `"db": "conectada"`?

Si llegaste acá: **migraste una API de memoria a una base de datos real** en
una clase. Eso es un hito de carrera, no de tarea.

### F.4 La lección profesional: tu base se puede "dormir"

Una aclaración sobre Supabase free tier que te va a ahorrar un susto:

> ⏰ Los proyectos de Supabase free tier se **pausan** después de **7 días sin
> actividad**. No perdés nada: los datos quedan intactos. Para despertarla:
> entrás al dashboard, abrís tu proyecto y click en **Restore** / **Reactivate**
> (un solo click, se reactiva en unos minutos).

Dato profesional, no solo de Supabase: los recursos free y de prueba se pausan
cuando no se usan — es la forma en que las nubes controlan costos. Cuando
trabajes en una empresa, la base de producción jamás se duerme: paga por estar
arriba 24/7. La lógica económica es la misma que la nuestra, con ceros de más.

---

## Resumen de archivos creados

| # | Archivo | Ubicación | Para qué |
|---|---------|-----------|----------|
| 1 | `pyproject.toml` | `backend/` | Declara dependencias nuevas: `psycopg`, `psycopg-pool`, `python-dotenv` |
| 2 | `schema.sql` | `backend/` | Crea la tabla `tasks` (el molde de los datos) |
| 3 | `.env` | `backend/` | Guarda `DATABASE_URL` (tu connection string del pooler) — NO se sube al repo |
| 4 | `main.py` | `backend/` | La misma API del Módulo 01, ahora con SQL real |

**¿Los tenés todos?** ¡Felicitaciones — tu API ya no se olvida de nada! 🎉

---

## Ejercicios para después de clase

### Nivel 🟢 Comprensión
1. Mirá el health check: ejecuta `SELECT COUNT(*) AS total FROM tasks`. ¿Qué
   devuelve y por qué sirve para saber si la base está viva? ¿Para qué
   serviría en un sistema real con monitores?
2. Cambiá `max_length=200` a `max_length=5` en `TaskCreate` y creá una tarea
   de 10 caracteres. ¿Qué error devuelve la API (422)? ¿Y si cambiás el
   tamaño de `title` en la tabla con `ALTER TABLE`? ¿Quién "manda"?
3. En la consola SQL (Supabase o psql) ejecutá `INSERT INTO tasks (title)
   VALUES ('sin fecha')` y después `SELECT * FROM tasks`. ¿De dónde salió el
   `created_at`? ¿Y si ejecutás `UPDATE tasks SET title = NULL WHERE id = 1;`
   — ¿funciona? ¿Por qué?

### Nivel 🟡 Aplicación
4. Agregá una columna `priority` (`TEXT NOT NULL DEFAULT 'media'`) a la tabla
   con `ALTER TABLE`, agregala al modelo Pydantic y al `serialize_task`, y
   mandá `priority` en el POST. Ejercicio completo de **schema → modelo →
   endpoint**: el contrato de la API crece en las tres capas.
5. Agregá un endpoint `GET /api/tasks/stats` que devuelva:
   `{"total": X, "completadas": Y, "pendientes": Z}` usando
   `COUNT(*)` con `WHERE completed = TRUE` y `WHERE completed = FALSE`.
6. Borrá la línea `conn.row_factory = dict_row` de un endpoint y probalo.
   ¿Qué cambia en el error? ¿Podés acceder a `row["id"]` ahora?

### Nivel 🔴 Análisis
7. **El experimento de la inyección SQL** (hacelo en una base de pruebas, no
   en producción): en Postman, creá una tarea con este título:
   `'); DROP TABLE tasks; --`
   Observá que **no pasa nada** — la tabla sigue viva. Ahora probá
   imaginariamente qué pasaría si el código usara
   `cur.execute(f"INSERT INTO tasks (title) VALUES ('{body.title}')")`.
   ¿Por qué `%s` te protege? (Pista: psycopg envía el valor como **dato
   parametrizado**, nunca como parte del SQL.)
8. Convertí los endpoints de `def` (síncronos) a `async def` y cambiá `psycopg`
   por `asyncpg` (usando `asyncpg.create_pool`). Compará cómo cambian los
   `cursor.execute` → `await pool.fetch/fetchrow/execute`. ¿Qué gana un
   servidor asíncrono con una base de datos en un escenario con miles de
   requests?
9. Agregá una restricción `CHECK (char_length(title) > 0)` en la tabla y
   manejá el error que lanza PostgreSQL cuando llega un título vacío: probalo
   mandando `""` desde Postman. ¿Qué status code tendría que devolver la API?
   ¿Cómo se detecta una `psycopg.errors` de check violation en el código?

---

## Resumen de la clase

| Fase | Tiempo | Qué aprendimos |
|------|--------|----------------|
| Fase 1 — El hook | 5' | Los datos en una lista de Python mueren cuando reinicia el servidor. Por eso existen las bases de datos (persistencia). |
| Fase 2 — Dos caminos | 15' | PostgreSQL es el motor; Docker lo levanta local, Supabase lo da gratis en la nube. Solo cambia la connection string. |
| Fase 3 — SQL en 10 min | 10' | `CREATE TABLE` define el molde; INSERT/SELECT/UPDATE/DELETE son el CRUD. `WHERE` sin filtro = peligro. |
| Fase 4 — La conexión | 10' | Anatomía de la connection string, `.env` para secretos, pools de conexiones (analogía del estacionamiento), psycopg. |
| Fase 5 — Migrar la API | 35' | `%s` vs inyección SQL, `RETURNING`, toggle con `NOT completed`, `dict_row`, `serialize_task`, `lifespan`. Mismo contrato, motor nuevo. |
| Fase 6 — Cierre | 15' | Los datos sobreviven al reinicio. El frontend del Módulo 01 funciona sin tocar una línea. El contrato de la API es la clave. |

---

> *En la clase 01 aprendiste a hablarle a un proceso que vivía en tu máquina.
> Hoy aprendiste a hablarle a una base que vive en la nube. La universidad te
> da el mapa. El recorrido lo hacés vos.*
