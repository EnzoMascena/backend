# Módulo 03 — Arquitectura en Capas + ORM + TypeScript

> **Materia**: Desarrollo de Software
> **Duración**: 60 minutos (taller por grupos, aula invertida)
> **Metodología**: descubrimiento guiado — los alumnos construyen, el docente pregunta

---

## Material del aula

| Archivo | Para quién | Qué es |
|---------|------------|--------|
| [`MATERIAL_PREVIO.md`](./MATERIAL_PREVIO.md) | Alumnos | **Lectura pre-clase** (aula invertida): capas, ORM, SQLModel, TypeScript |
| [`GUIA_DOCENTE.md`](./GUIA_DOCENTE.md) | Docente | **Conducción** del taller: timeline, checkpoints, desbloqueo |
| [`GUIA_ALUMNO.md`](./GUIA_ALUMNO.md) | Alumnos | **Actividad por grupos**: scaffold + consignas + solución de referencia |
| [`PRESENTACION.md`](./PRESENTACION.md) | Docente | **Guía paso a paso** proyectada (slides Marp) |
| [`SPEC.md`](./SPEC.md) | Todos | Especificación completa del software |
| [`postman/`](./postman/) | Todos | Collection con tests (flujo feliz + casos límite) |

> **Flujo del aula**: los alumnos leyeron `MATERIAL_PREVIO` en casa. En clase
> reciben el scaffold y completan tres archivos por descubrimiento, guiados por
> `GUIA_ALUMNO.md`. El docente conduce con `GUIA_DOCENTE.md` y proyecta
> `PRESENTACION.md`.

---

## Objetivo del Taller

Refactorizar la API de Tareas del Módulo 02 en **tres capas** con
responsabilidades separadas, reemplazar el SQL crudo por un **ORM**
(SQLModel) y migrar el frontend a **TypeScript**.

| | Módulo 02 | Módulo 03 |
|---|---|---|
| Estructura | `main.py` monolítico (~300 líneas) | 3 capas separadas |
| Acceso a datos | SQL crudo (psycopg) | **ORM (SQLModel)** |
| Esquema | `schema.sql` manual | Generado por el modelo (`create_all`) |
| CRUD | 4 endpoints + toggle | **CRUD completo** (+GET by id, +editar título) |
| Frontend | JavaScript | **TypeScript** |
| Contrato de API | — | Mismos campos, `created_at` ISO 8601 |

---

## Arquitectura

```
Frontend (TS) ── HTTP/JSON ──► Controller ──► Service ──► Repository ──► PostgreSQL
  :5173                         (FastAPI)     (negocio)     (SQLModel)     (Docker/Supabase)
  tipos = contrato               HTTP          reglas        ORM
```

**Regla de dependencia**: cada capa solo conoce a la de abajo.

```
app/
├── main.py                    # entrypoint: app + routers + lifespan
├── database.py                # engine + session + create_all
├── dependencies.py            # inyección de dependencias (Depends)
├── models/task.py             # SQLModel: Task, TaskCreate, TaskUpdate, TaskRead
├── repositories/task_repository.py   # ORM: select, get, add, update, delete
├── services/task_service.py          # reglas de negocio (strip, "no existe")
└── controllers/
    ├── task_controller.py     # endpoints /api/tasks (el 404 vive acá)
    └── health_controller.py   # /api/health
```

---

## Endpoints (CRUD completo)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/health` | Health check (consulta la base) |
| `GET` | `/api/tasks` | Listar tareas |
| `POST` | `/api/tasks` | Crear tarea |
| `GET` | `/api/tasks/{id}` | Leer UNA tarea |
| `PATCH` | `/api/tasks/{id}` | Actualizar título y/o estado |
| `DELETE` | `/api/tasks/{id}` | Eliminar tarea |

---

## Instalación

### Backend

```bash
cd backend
cp .env.example .env        # completá DATABASE_URL (podés reusar la del Módulo 02)
uv sync
uv run -m app.main          # http://localhost:8000
```

> **La tabla se crea sola** al arrancar (`SQLModel.metadata.create_all`). Ya no
> hay `schema.sql`. Si reutilizás la base del Módulo 02, la tabla `tasks` ya
> existe y el ORM la mapea tal cual (es idempotente).

### Frontend

```bash
cd frontend
pnpm install
pnpm dev                    # http://localhost:5173 (proxy → :8000)
```

---

## Entendiendo el código: la lección en una tabla

| Responsabilidad | Módulo 02 (monolito) | Módulo 03 (capas) |
|-----------------|---------------------|-------------------|
| Validación | Pydantic en el endpoint | `models/task.py` |
| SQL | dentro de los endpoints | `repositories/task_repository.py` |
| Regla de negocio (`strip`, "no existe") | dentro de los endpoints | `services/task_service.py` |
| HTTP (rutas, 404, status codes) | mezclado | `controllers/task_controller.py` |
| Conexión | `pool` arriba del main | `database.py` |
| Cableado | implícito | `dependencies.py` |

**El `404` vive en el controller** (es HTTP). El service devuelve `Task | None`
(o `bool`) y no conoce los status codes. **El `strip()` vive en el service**
(es negocio). **El SQL vive en el repository** (vía ORM).

---

## Diferencias clave vs Módulo 02

| Aspecto | Módulo 02 | Módulo 03 |
|---------|-----------|-----------|
| Consulta de todas | `cur.execute("SELECT ... FROM tasks")` | `session.exec(select(Task).order_by(Task.id))` |
| Leer por id | `WHERE id = %s` | `session.get(Task, id)` |
| Crear | `INSERT ... RETURNING` | `session.add(task)` + `commit` |
| Actualizar | `UPDATE ... SET completed = NOT completed` | `setattr` + `commit` (parcial) |
| Serializar fecha | `serialize_task()` manual | SQLModel/Pydantic automático |
| Esquema | `schema.sql` a mano | `create_all` desde el modelo |

---

## Ejercicios para Llevar a Casa

### Nivel 🟢 Comprensión

1. Explicá la regla de dependencia entre capas con tus palabras.
2. ¿Por qué el service no puede devolver un `404`? ¿Dónde vive y por qué?
3. ¿Qué SQL que escribías a mano en el Módulo 02 ahora escribe el ORM?

### Nivel 🟡 Aplicación

4. Agregá `GET /api/tasks?completed=true` (filtro) end-to-end: repository →
   service → controller → frontend.
5. Agregá un campo `priority` al modelo SQLModel. ¿Qué cambia en el `create_all`
   si la tabla ya existe? (investigá por qué NO se agrega la columna).
6. En el frontend, agregá un botón "filtrar completadas" usando el tipo `Task`.

### Nivel 🔴 Análisis

7. ¿Qué harías para que el service lance una excepción de dominio
   (`TaskNotFoundError`) en vez de devolver `None`? ¿Dónde la traducirías a 404?
   Investigá `app.add_exception_handler`.
8. El ORM genera SQL por vos. Activá `echo=True` en el `create_engine` y mirá
   qué SQL se ejecuta. ¿Lo reconocés del Módulo 02?
9. Investigá qué son las **migraciones** (Alembic) y por qué `create_all` no
   alcanza cuando el esquema cambia en producción.

---

## Referencias

- [SQLModel — Documentación](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy 2.0 — Documentación](https://docs.sqlalchemy.org/en/20/)
- [FastAPI — Dependencias](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI — SQLModel](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [TypeScript — Documentación](https://www.typescriptlang.org/docs/)
- [React + TypeScript](https://react.dev/learn/typescript)
- [Vite — Documentación](https://vite.dev/)
