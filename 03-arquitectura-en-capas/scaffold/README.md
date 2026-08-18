# 🧱 Scaffold — Módulo 03 (versión para entregar a los grupos)

> **Para el docente.** Esta carpeta contiene los **3 archivos incompletos**
> que los grupos deben completar por descubrimiento. El resto del backend
> (modelos, conexión, cableado, main, health) se entrega completo.

## Cómo usarlo

1. Entregá a cada grupo el backend completo del módulo 03, **pero con estos
   3 archivos reemplazando a los originales**:

   | Archivo del scaffold | Reemplaza a… |
   |----------------------|--------------|
   | `app/repositories/task_repository.py` | `backend/app/repositories/task_repository.py` |
   | `app/services/task_service.py` | `backend/app/services/task_service.py` |
   | `app/controllers/task_controller.py` | `backend/app/controllers/task_controller.py` |

2. Cada archivo tiene la **firma completa** (con type hints y docstrings) y el
   cuerpo con `raise NotImplementedError("TODO: ...")`.

3. Los grupos completan los `TODO` siguiendo las consignas de `GUIA_ALUMNO.md`
   (que es su material de trabajo). No les des estos 3 archivos completos
   hasta el final.

> 💡 **Consejo**: si usás GitHub Classroom o un repo base, entregá esta
> versión incompleta como rama principal y guardá la solución en una rama
> `solucion` que desbloqueás al cierre.

## Qué tiene cada esqueleto

- **`task_repository.py`** — los 6 métodos del CRUD con el ORM (`select`,
  `session.get`, `add/commit/refresh`, `model_dump(exclude_unset=True)`).
  El `count()` viene resuelto como ejemplo.
- **`task_service.py`** — la lógica de negocio. La decisión clave: cuando la
  tarea no existe, devuelve `None`/`False` (no lanza 404 — eso es HTTP).
- **`task_controller.py`** — los 5 endpoints. Traduce `None` → `404` con
  `raise HTTPException`. Mirá `health_controller.py` como ejemplo vivo.
