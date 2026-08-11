# Módulo 02 — Persistencia con PostgreSQL

> **Materia**: Desarrollo de Software
> **Duración**: 90 minutos
> **Taller guiado**: Sí — construcción **desde cero**, archivo por archivo, sin clonar el repo

---

## Material del aula

| Archivo | Para quién | Qué es |
|---------|------------|--------|
| [`GUIA_ALUMNO.md`](./GUIA_ALUMNO.md) | Alumnos | **Material de trabajo**. Código completo en orden de creación, con tiempos y checkpoints. Cada alumno la abre en su navegador y copia los archivos. |
| [`PRESENTACION.md`](./PRESENTACION.md) | Docente | Slides Marp (fases, comandos clave, checkpoints) |
| `README.md` | Todos | **Esta guía de referencia**. Instalación multi-OS y explicación del código. |
| [`SPEC.md`](./SPEC.md) | Todos | Especificación completa del software |
| [`postman/`](./postman/) | Todos | Collection con tests automáticos (flujo feliz + casos límite) |

> **Flujo del aula**: los alumnos construyen el backend a mano siguiendo `GUIA_ALUMNO.md`. Este README queda como referencia de instalación y para entender el código.

---

## Objetivo del Taller

La **misma API de Tareas del Módulo 01**, pero con los datos en **PostgreSQL** de verdad. En el camino cubrimos:

- Por qué una lista en memoria no sirve para datos reales
- Mini intro a Docker (demo del docente)
- SQL básico: `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- La conexión: connection string, `DATABASE_URL`, pool de conexiones
- Migrar la API: de `tasks: list[dict]` a consultas SQL reales
- **El contrato de la API intacto**: el frontend de la clase 01 funciona sin cambios

## Qué vamos a construir

Mismos 4 endpoints del Módulo 01 — **el contrato no cambia**:

| Operación | HTTP | Endpoint | Descripción |
|-----------|------|----------|-------------|
| Listar | `GET` | `/api/tasks` | Devuelve todas las tareas |
| Crear | `POST` | `/api/tasks` | Crea una tarea nueva |
| Completar | `PATCH` | `/api/tasks/{id}` | Marca como hecha / desmarca |
| Eliminar | `DELETE` | `/api/tasks/{id}` | Borra una tarea |

**Lo que cambia**: el motor de almacenamiento.

| | Módulo 01 | Módulo 02 |
|---|---|---|
| Dónde viven los datos | Lista de Python en memoria | Tabla en PostgreSQL |
| ¿Sobreviven al reinicio? | ❌ Se pierden | ✅ Persisten |
| ¿Quién genera el `id`? | Python (`next_id`) | La base (`IDENTITY`) |
| ¿Quién genera `created_at`? | Python | La base (`DEFAULT NOW()`) |

## Arquitectura

```
┌─────────────────┐   HTTP    ┌─────────────────┐    SQL     ┌──────────────┐
│   Frontend 01   │ ────────► │   Backend 02    │ ────────►  │  PostgreSQL  │
│   React + Vite  │  JSON     │   FastAPI       │  psycopg    │  (Docker o   │
│   :5173         │ ◄──────── │   :8000         │ ◄───────── │   Supabase)  │
│   (SIN CAMBIOS) │           │   pool          │            │              │
└─────────────────┘           └─────────────────┘            └──────────────┘
```

---

## Estructura del Módulo

```
02-persistencia-postgresql/
├── README.md                    # Esta guía de referencia
├── GUIA_ALUMNO.md               # Material de aula — código completo desde cero
├── SPEC.md                      # Especificación del software
├── PRESENTACION.md              # Slides Marp (fases + checkpoints)
│
├── backend/
│   ├── pyproject.toml           # Dependencias Python (uv)
│   ├── schema.sql               # Esquema de la base (CREATE TABLE)
│   ├── .env.example             # Plantilla de configuración (¡copiar a .env!)
│   └── main.py                  # API con persistencia (~230 líneas)
│
└── postman/
    └── 02-persistencia-postgresql.postman_collection.json
```

> **Nota sobre el frontend**: el frontend es el del Módulo 01 (`../01-mi-primera-app/frontend`). **No se toca.** Eso es la lección: una API estable es un contrato.

---

# PARTE 1 — Preparación de la Base de Datos

> **IMPORTANTE**: el backend usa una **URL de conexión** (`DATABASE_URL`). La URL dice dónde vive postgres. Hay dos caminos — el docente demuestra Docker, los alumnos usan Supabase. **El código del backend es el mismo para ambos**, solo cambia la URL.

## 1.1 Opción docente — PostgreSQL con Docker (demo)

```bash
# Descargar y correr postgres 16 en un contenedor
docker run -d --name pg-clase02 \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16-alpine

# Verificar que está vivo
docker exec pg-clase02 pg_isready -U postgres
# → /var/run/postgresql:5432 - accepting connections

# Ver contenedores corriendo
docker ps

# Entrar a la consola de postgres (psql)
docker exec -it pg-clase02 psql -U postgres
```

**Conceptos mínimos de Docker** (todo lo que necesitamos hoy):

| Concepto | Qué es | Comando |
|----------|--------|---------|
| **Imagen** | El "molde" — postgres ya instalado y configurado | `postgres:16-alpine` |
| **Contenedor** | Una instancia corriendo de esa imagen | `docker run` |
| **Puerto** | La puerta de entrada: `5432` local → `5432` del contenedor | `-p 5432:5432` |
| **Variable de entorno** | Cómo le pasamos la contraseña al arrancar | `-e POSTGRES_PASSWORD=...` |

Analogía: una imagen es un **módulo prefabricado** — viene con todo adentro (el motor de postgres instalado y listo). El contenedor es ese módulo **enchufado y funcionando** en tu máquina. No instalaste nada en tu sistema.

## 1.2 Opción alumno — Supabase free tier

1. Creá una cuenta en [supabase.com](https://supabase.com) (plan **Free**, sin tarjeta)
2. Creá un proyecto nuevo (elegí la región más cercana, password fuerte)
3. Andá a **Settings → Database → Connection string**
4. Copiá la URL del **pooler** (Transaction — puerto 6543):
   `postgresql://postgres.TU_REF:TU_PASSWORD@aws-0-TU_REGION.pooler.supabase.com:6543/postgres`

> 💡 **¿Por qué el pooler y no la conexión directa?** La conexión directa de Supabase usa IPv6 en muchos casos, y las redes universitarias suelen ser solo IPv4. El pooler funciona por IPv4 — más confiable en el aula. Y de paso ya conocés el concepto de pool, que usamos en el backend.

> 🧨 **Gotcha profesional (contalo en clase)**: el free tier de Supabase **pausa** el proyecto tras 7 días sin actividad. Los datos NO se pierden — reactivás con un click (tenés 90 días). Es una lección real: el free tier tiene límites operativos, no solo de espacio.

## 1.3 Crear la tabla (schema.sql)

El esquema define el **molde** de los datos. Ejecutalo **una sola vez**:

```bash
# Docker
docker exec -i pg-clase02 psql -U postgres < schema.sql

# Supabase: Dashboard → SQL Editor → pegar el contenido → Run
```

Verificar que la tabla existe:

```bash
docker exec pg-clase02 psql -U postgres -c "\d tasks"
```

---

# PARTE 2 — Backend (FastAPI + uv + psycopg)

## 2.1 Crear el proyecto

**En el aula**: seguí `GUIA_ALUMNO.md` — creás los archivos a mano (`pyproject.toml`, `schema.sql`, `.env`, `main.py`), en ese orden.

```bash
mkdir -p 02-persistencia-postgresql/backend
cd 02-persistencia-postgresql/backend
```

## 2.2 Instalar dependencias

```bash
uv sync
```

Esto crea el entorno virtual `.venv` e instala FastAPI, uvicorn, **psycopg** (el driver de PostgreSQL) y **psycopg-pool** (el pool de conexiones).

## 2.3 Configurar la conexión

```bash
cp .env.example .env
# Y editá .env con TU URL (Docker o Supabase, según tu caso)
```

## 2.4 Ejecutar el servidor

```bash
uv run main.py
```

Deberías ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

> Si el arranque falla con un error de conexión, el pool se abrió en el `lifespan` y no pudo hablar con postgres. Revisá la `DATABASE_URL` — ese es el síntoma clásico.

## 2.5 Verificar

```bash
# Swagger
http://localhost:8000/docs

# Health (ahora consulta la base de verdad)
curl http://localhost:8000/api/health
# → {"status":"Funciona","service":"02-...","db":"conectada","tasks_count":0}

# Crear una tarea
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender SQL"}'
```

## 2.6 El momento de la clase — persistencia

```bash
# 1. Creá varias tareas
# 2. Matá el servidor (Ctrl+C)
# 3. Volvé a ejecutar uv run main.py
# 4. Listá las tareas
curl http://localhost:8000/api/tasks
```

**Los datos siguen ahí.** En el Módulo 01, ese reinicio significaba volver a cero. Hoy los datos viven en PostgreSQL, no en el proceso de Python.

## 2.7 Probar con Postman

Importá la collection [`02-persistencia-postgresql.postman_collection.json`](./postman/) (tiene tests automáticos). El request **"7. PERSISTENCIA — reiniciá el servidor"** es el corazón de la clase.

---

# PARTE 3 — Entendiendo el Código

## La conexión

```python
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10, open=False)
```

**La URL de conexión es "la dirección completa"** de la base:

```
postgresql://  USUARIO  :  CONTRASEÑA  @  HOST  :  PUERTO  /  BDD
^protocolo    ^usuario     ^clave        ^dónde      ^puerta  ^nombre
```

**¿Por qué un pool?** Abrir una conexión cuesta (handshake TCP, autenticación, SSL). Si cada request abriera una, saturaríamos postgres y perderíamos tiempo. El pool mantiene conexiones abiertas y las reutiliza: `min_size=1` siempre hay una lista, `max_size=10` tope de simultáneas. Se abre **una vez** en el `lifespan` (arranque del servidor) y se cierra al apagarse.

## El patrón SQL que se repite

```python
with pool.connection() as conn:
    conn.row_factory = dict_row          # cada fila llega como {"columna": valor}
    with conn.cursor() as cur:
        cur.execute("... SQL ...", (params,))
        row = cur.fetchone()
```

| Pieza | Para qué |
|-------|----------|
| `with pool.connection()` | Pedir conexión prestada. Al salir: **commit automático** (rollback si hubo error) y devolución al pool |
| `dict_row` | Postgres devuelve filas; con `dict_row` las leés por nombre: `row["title"]` |
| `%s` | **Placeholder** de parámetros. Nunca concatenar strings en SQL — es la puerta a la **inyección SQL** |
| `RETURNING` | Postgres devuelve la fila afectada — no hace falta una segunda consulta |

## El contrato intacto

`serialize_task()` convierte la fila de postgres al JSON del Módulo 01 (el `datetime` de `TIMESTAMPTZ` → string ISO). Los modelos Pydantic y los errores 404/422 son idénticos. **El frontend de la clase 01 no cambia ni una línea.**

---

# PARTE 4 — Diferencias clave vs Módulo 01

| Aspecto | Módulo 01 | Módulo 02 |
|---------|-----------|-----------|
| Storage | `tasks: list[dict]` | Tabla `tasks` en PostgreSQL |
| ID | `next_id` en Python | `GENERATED ALWAYS AS IDENTITY` |
| Fecha | `datetime.now(timezone.utc)` en Python | `DEFAULT NOW()` en la base |
| Toggle | `task["completed"] = not task["completed"]` | `UPDATE ... SET completed = NOT completed` |
| No encontrada | Recorrer la lista | `WHERE id = %s` → 0 filas → 404 |
| Health | Contaba la lista | `SELECT COUNT(*)` contra postgres |
| Ciclo de vida | Muere con el proceso | Sobrevive a todo |

---

# Ejercicios para Llevar a Casa

### Nivel 🟢 Comprensión

1. Explicá qué hace `SELECT 1` en el health check y por qué prueba la conexión.
2. ¿Qué pasa si cambiás `max_length=200` a `max_length=50` en `TaskCreate`? ¿Quién devuelve el 422, Pydantic o postgres?
3. ¿Por qué el frontend del Módulo 01 funciona sin cambios? Respondé usando la palabra "contrato".

### Nivel 🟡 Aplicación

4. Agregá una columna `priority` (`baja`/`media`/`alta`) end-to-end: `schema.sql` → modelo → endpoint → verificá con Postman.
5. Agregá `GET /api/tasks/stats` que devuelva `{ total, completed, pending }` usando `COUNT(*)` con `WHERE`.
6. En el SQL Editor de Supabase, escribí un `UPDATE` que marque todas las tareas como completadas de una sola vez.

### Nivel 🔴 Análisis

7. **Inyección SQL (experimento seguro)**: en Postman, probá `{"title": "'); DROP TABLE tasks; --"}`. ¿Qué pasa? Explicá por qué el `%s` te protege. Luego probá `{"title": "x' OR '1'='1"}` en un endpoint y analizá.
8. Reemplazá el pool síncrono por `AsyncConnectionPool` + endpoints `async def` y `psycopg.AsyncConnection`. Compará el código.
9. Agregá una `CHECK (length(title) BETWEEN 1 AND 200)` a la tabla. Ahora la BBDD también valida. ¿Qué pasa si la validación de Pydantic falla antes? ¿Y si la de la base falla? Reflexioná sobre "defensa en profundidad".

---

# Referencias

- [PostgreSQL — Documentación](https://www.postgresql.org/docs/)
- [psycopg 3 — Documentación](https://www.psycopg.org/psycopg3/docs/)
- [psycopg_pool — Documentación](https://www.psycopg.org/psycopg3/docs/api/pool.html)
- [Supabase — Free project pausing](https://supabase.com/docs/guides/platform/free-project-pausing)
- [FastAPI — Lifespan](https://fastapi.tiangolo.com/advanced/events/)
- [FastAPI — CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [uv — Documentación](https://docs.astral.sh/uv/)
- [Docker — Documentación](https://docs.docker.com/)
