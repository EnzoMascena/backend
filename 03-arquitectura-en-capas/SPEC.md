# SPEC — Módulo 03: Arquitectura en Capas + ORM + TypeScript

> **Versión**: 1.0.0
> **Estado**: ✅ Implementado y probado
> **Depende de**: Módulo 02 (persistencia con PostgreSQL) y Módulo 01 (contrato de la API)

---

## 1. Propósito

Refactorizar la API de Tareas del Módulo 02 en **tres capas** con responsabilidades separadas (Controller → Service → Repository), reemplazar el SQL crudo de psycopg por un **ORM** (SQLModel) y migrar el frontend de JavaScript a **TypeScript**.

El **contrato de la API se mantiene** en sus operaciones existentes y se **extiende** a un CRUD completo (se agrega lectura individual y actualización del título).

## 2. Alcance

### Dentro del alcance

- Backend organizado en 3 capas: `controllers/`, `services/`, `repositories/`
- Modelo de datos con **SQLModel** (ORM), que reemplaza el `schema.sql` manual
- CRUD completo: listar, crear, leer una, actualizar (título y/o estado) y eliminar
- Inyección de dependencias con `Depends()` de FastAPI (Session → Repository → Service)
- Frontend **React + Vite + TypeScript** con tipos que reflejan el contrato de la API
- Health check que consulta la base a través de las capas

### Fuera del alcance (módulos futuros)

- Migraciones formales con Alembic (este módulo usa `SQLModel.metadata.create_all`)
- Autenticación JWT / RBAC
- Testing automatizado con pytest (se deja la base sentada para el módulo de testing)
- Dockerización del backend

## 3. Requisitos Funcionales

| ID | Requisito |
|----|-----------|
| RF-01 | `GET /api/tasks` lista todas las tareas ordenadas por `id` |
| RF-02 | `POST /api/tasks` crea una tarea; el `id` y `created_at` los genera la base, `completed` arranca en `false` |
| RF-03 | `GET /api/tasks/{id}` devuelve UNA tarea; 404 si no existe |
| RF-04 | `PATCH /api/tasks/{id}` actualiza `title` y/o `completed` (parcial); 404 si no existe |
| RF-05 | `DELETE /api/tasks/{id}` elimina la tarea; `{ "ok": true }` si existía, 404 si no |
| RF-06 | `GET /api/health` reporta `db: "conectada"` y el conteo de tareas |
| RF-07 | El frontend TypeScript consume el CRUD completo (crear, listar, editar, toggle, eliminar) |

## 4. Requisitos No Funcionales

| ID | Requisito |
|----|-----------|
| RNF-01 | **Mantenibilidad**: cada archivo tiene UNA responsabilidad (separación por capas) |
| RNF-02 | **Testeabilidad**: las capas son intercambiables vía inyección de dependencias |
| RNF-03 | **Seguridad**: sin SQL concatenado — el ORM parametriza las consultas automáticamente |
| RNF-04 | **Compatibilidad**: mismo contrato JSON que los módulos anteriores (`id`, `title`, `completed`, `created_at` ISO 8601) |
| RNF-05 | **Configurabilidad**: `DATABASE_URL` por `.env`, sin credenciales en el código |
| RNF-06 | **Tipado estático (frontend)**: TypeScript con `strict: true` |

## 5. Modelo de Datos (SQLModel)

```python
class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
```

| Clase | Rol | table=True | Uso |
|-------|-----|-----------|-----|
| `TaskBase` | Campos comunes (title) | no | Base de herencia |
| `Task` | La TABLA (mapea `tasks`) | **sí** | Persistencia (ORM) |
| `TaskCreate` | Entrada al crear (solo title) | no | `POST` |
| `TaskUpdate` | Entrada al actualizar (campos opcionales) | no | `PATCH` |
| `TaskRead` | Salida (tarea completa) | no | `response_model` |

**Decisión**: `created_at` lo genera **la base** (`server_default=func.now()`), manteniendo la lección del Módulo 02 ("la base es la fuente de verdad").

## 6. Arquitectura

```
Frontend (TS) ── HTTP/JSON ──► Controller ──► Service ──► Repository ──► PostgreSQL
  :5173                         (FastAPI)     (negocio)     (SQLModel)     (Docker/Supabase)
  tipos = contrato               HTTP          reglas        ORM
```

### Regla de dependencia (la lección central)

```
Controller ──► Service ──► Repository ──► Base de datos
   (HTTP)        (negocio)     (ORM/SQL)
```

Cada capa **solo conoce a la que está debajo**. Nunca hacia arriba ni en diagonal.

| Capa | Carpeta | Sabe de… | NO sabe de… |
|------|---------|----------|-------------|
| Controller | `controllers/` | HTTP, status codes, rutas | SQL, reglas de negocio |
| Service | `services/` | reglas de negocio | HTTP, SQL |
| Repository | `repositories/` | SQL/ORM, la base | HTTP, negocio |
| Modelos | `models/` | la tabla (SQLModel) | — |

### Dónde vive cada responsabilidad

| Responsabilidad | Módulo 02 (monolito) | Módulo 03 (capas) |
|-----------------|---------------------|-------------------|
| Validación de entrada | Pydantic en el endpoint | `models/task.py` |
| Acceso a datos (SQL) | dentro de los endpoints | `repositories/task_repository.py` |
| Regla de negocio (`strip`, "no existe") | dentro de los endpoints | `services/task_service.py` |
| HTTP (rutas, status codes, 404) | mezclado | `controllers/task_controller.py` |
| Conexión / engine | arriba del main | `database.py` |
| Cableado entre capas | implícito | `dependencies.py` |

**Decisión clave**: el `404` vive en el **controller** (es HTTP). El service devuelve `Task | None` (o `bool`) y no conoce qué es un status code.

## 7. Endpoints

### Flujo feliz

| # | Método | Ruta | Body | Respuesta |
|---|--------|------|------|-----------|
| 1 | `GET` | `/api/health` | — | `200` `{status, service, db, tasks_count}` |
| 2 | `GET` | `/api/tasks` | — | `200` `Task[]` |
| 3 | `POST` | `/api/tasks` | `{"title": "..."}` | `201` `Task` |
| 4 | `GET` | `/api/tasks/{id}` | — | `200` `Task` |
| 5 | `PATCH` | `/api/tasks/{id}` | `{"completed": true}` o `{"title": "..."}` | `200` `Task` |
| 6 | `DELETE` | `/api/tasks/{id}` | — | `200` `{"ok": true}` |

### Errores

| Caso | Código | Body |
|------|--------|------|
| `title` vacío / > 200 / no string / faltante | `422` | error Pydantic |
| GET/PATCH/DELETE de id inexistente | `404` | `{"detail": "Tarea {id} no encontrada"}` |
| Base caída | `500` | error de conexión |

## 8. Configuración

`.env` (copiado desde `.env.example`), misma `DATABASE_URL` que el Módulo 02. Se puede **reutilizar la base del Módulo 02**: la tabla `tasks` ya existe y el ORM la mapea tal cual (`create_all` es idempotente).

## 9. Verificación

- **Prueba de lógica** (SQLite in-memory): CRUD completo verificado — `strip`, update parcial sin pisar campos, `None`/`False` en ids inexistentes.
- **Collection Postman**: flujo feliz (6 requests) + casos límite (422/404).
- **Frontend**: `pnpm dev` contra el backend, CRUD end-to-end con edición de título.
