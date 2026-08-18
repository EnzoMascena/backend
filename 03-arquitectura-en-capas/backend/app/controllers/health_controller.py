"""
Health check — capa de presentación.

Vive en su propio controller porque es una responsabilidad distinta a
las tareas. Si el health cambia, no tocamos el controller de tareas.
Así cada archivo tiene UNA razón para cambiar.
"""

from fastapi import APIRouter, Depends

from app.dependencies import get_task_service
from app.services.task_service import TaskService

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health_check(service: TaskService = Depends(get_task_service)):
    """GET /api/health — verifica que el servicio y la base responden."""
    return {
        "status": "Funciona",
        "service": "03-arquitectura-en-capas-backend",
        "db": "conectada",
        "tasks_count": service.count_tasks(),
    }
