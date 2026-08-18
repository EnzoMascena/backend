"""
Capa de presentación (Controller) — los endpoints HTTP.

COMPLETÁ los endpoints marcados con TODO. El controller:
  - recibe el request y delega en el service
  - traduce `None` (o `False`) del service a un `404` con HTTPException
  - NO toca la base ni aplica reglas de negocio

MIRÁ `health_controller.py` (ya viene resuelto): es tu ejemplo de cómo
recibir el service con `Depends(get_task_service)`.

Endpoints a implementar:
  GET    /api/tasks           → list_tasks
  POST   /api/tasks           → create_task (status 201)
  GET    /api/tasks/{task_id} → get_task
  PATCH  /api/tasks/{task_id} → update_task
  DELETE /api/tasks/{task_id} → delete_task
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_service
from app.models.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(service: TaskService = Depends(get_task_service)):
    raise NotImplementedError("TODO: implementar list_tasks")


# TODO: agregá acá los endpoints que faltan:
#   - GET /{task_id}
#   - POST ""
#   - PATCH /{task_id}
#   - DELETE /{task_id}
#
# Recordá: cuando el service devuelve None (o False), acá se traduce a 404:
#
#   if task is None:
#       raise HTTPException(
#           status_code=status.HTTP_404_NOT_FOUND,
#           detail=f"Tarea {task_id} no encontrada",
#       )
