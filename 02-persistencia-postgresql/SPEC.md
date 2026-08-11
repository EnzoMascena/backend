# SPEC — Módulo 02: Persistencia con PostgreSQL

> **Versión**: 1.0.0
> **Estado**: ✅ Implementado y probado
> **Depende de**: Módulo 01 (contrato de API + frontend reutilizado)

---

## 1. Propósito

Agregar **persistencia real** a la API de Tareas del Módulo 01. Los datos que antes vivían en una lista de Python en memoria pasan a vivir en **PostgreSQL**. La API **no cambia su contrato externo**: mismos endpoints, mismos campos, mismos códigos de error.

## 2. Alcance

### Dentro del alcance

- Conexión a PostgreSQL vía `DATABASE_URL` (Docker local o Supabase free tier)
- Pool de conexiones (`psycopg_pool`) con ciclo de vida manejado por `lifespan`
- Tabla `tasks` con `CREATE TABLE IF NOT EXISTS` (idempotente)
- Migración de los 4 endpoints del CRUD de lista en memoria → SQL
- Health check que verifica la conexión real a la base (`SELECT COUNT(*)`)
- Contrato de API idéntico al Módulo 01 (frontend JS reutilizado sin cambios)

### Fuera del alcance (módulos futuros)

- Migraciones formales con Alembic
- Arquitectura en capas (Controller → Service → Repository)
- Autenticación / RBAC
- Dockerización del backend (solo se usa Docker para el postgres de la demo)
- Frontend en TypeScript

## 3. Requisitos Funcionales

| ID | Requisito |
|----|-----------|
| RF-01 | `GET /api/tasks` lista todas las tareas ordenadas por `id`, leyendo de PostgreSQL |
| RF-02 | `POST /api/tasks` inserta una tarea con `INSERT ... RETURNING`; el `id`, `completed` y `created_at` los genera la base |
| RF-03 | `PATCH /api/tasks/{id}` alterna `completed` con `UPDATE ... SET completed = NOT completed`; 404 si no existe |
| RF-04 | `DELETE /api/tasks/{id}` elimina la fila; `{ "ok": true }` si existía, 404 si no |
| RF-05 | `GET /api/health` ejecuta `SELECT COUNT(*) FROM tasks`; reporta `db: "conectada"` |
| RF-06 | Los datos sobreviven al reinicio del servidor (persistencia) |

## 4. Requisitos No Funcionales

| ID | Requisito |
|----|-----------|
| RNF-01 | **Seguridad**: toda consulta usa placeholders `%s` (protección contra inyección SQL) |
| RNF-02 | **Performance**: conexiones reutilizadas vía pool (min 1, max 10) |
| RNF-03 | **Compatibilidad**: mismo contrato JSON que el Módulo 01 (`id`, `title`, `completed`, `created_at` como ISO 8601) |
| RNF-04 | **Configurabilidad**: la URL de la base se configura por `.env` (sin credenciales en el código) |
| RNF-05 | **Portabilidad**: el mismo código funciona contra Docker y Supabase — solo cambia `DATABASE_URL` |

## 5. Modelo de Datos

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title       TEXT        NOT NULL,
    completed   BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

| Columna | Tipo | Fuente del valor | Notas |
|---------|------|------------------|-------|
| `id` | `INTEGER` | `IDENTITY` | Clave primaria, auto-incremental, generada por la base |
| `title` | `TEXT` | API (Pydantic valida 1..200) | `NOT NULL` |
| `completed` | `BOOLEAN` | `DEFAULT FALSE` | Toggle vía `NOT completed` |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Con zona horaria; se serializa a ISO 8601 |

**Decisión**: la base es la **fuente de verdad** para `id`, `completed` y `created_at`. El código Python ya no genera esos valores (diferencia clave vs Módulo 01).

## 6. Arquitectura

```
Frontend 01 (JS) ── HTTP/JSON ──► FastAPI (sync) ── psycopg ──► PostgreSQL
    :5173                            :8000         pool        (Docker/Supabase)
    sin cambios                      lifespan
```

- Endpoints **síncronos** (`def`): FastAPI los corre en el threadpool. Simple y suficiente para este alcance.
- **Pool**: `ConnectionPool(min_size=1, max_size=10, open=False)`, abierto en `lifespan` (startup) y cerrado en shutdown.
- **Fila → dict**: `conn.row_factory = dict_row` por conexión prestada.
- **Serialización**: `serialize_task()` convierte `datetime` de postgres a string ISO (contrato intacto).

## 7. Endpoints

### Flujo feliz

| # | Método | Ruta | Body | Respuesta esperada |
|---|--------|------|------|--------------------|
| 1 | `GET` | `/api/health` | — | `200` `{status, service, db: "conectada", tasks_count}` |
| 2 | `GET` | `/api/tasks` | — | `200` `[]` o lista de tareas |
| 3 | `POST` | `/api/tasks` | `{"title": "..."}` | `201` tarea completa |
| 4 | `PATCH` | `/api/tasks/{id}` | — | `200` tarea con `completed` alternado |
| 5 | `DELETE` | `/api/tasks/{id}` | — | `200` `{"ok": true}` |

### Errores (idénticos al Módulo 01)

| Caso | Código | Body |
|------|--------|------|
| `title` vacío | `422` | `string_too_short` |
| `title` > 200 chars | `422` | `string_too_long` |
| Sin `title` | `422` | `missing` |
| `title` no string | `422` | `string_type` |
| PATCH/DELETE id inexistente | `404` | `{"detail": "Tarea {id} no encontrada"}` |
| BBDD caída | `500` | error de conexión (pool) |

## 8. Configuración

`.env` (copiado desde `.env.example`):

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres   # Docker
DATABASE_URL=postgresql://postgres.REF:PASS@aws-0-REGION.pooler.supabase.com:6543/postgres  # Supabase
```

- `load_dotenv()` lee `.env`; default localhost por comodidad de demo.
- El `.env` está en `.gitignore` (contiene credenciales).

## 9. Verificación

- Collection Postman con tests automáticos: 8 requests de flujo feliz (incluye el request **PERSISTENCIA**: reiniciar el servidor y verificar que la tarea sobrevive) + 6 casos límite.
- Prueba manual de persistencia: crear tareas → `Ctrl+C` → `uv run main.py` → listar → las tareas siguen.
- Contrato: los errores 404/422 y los campos JSON son byte a byte iguales al Módulo 01.
