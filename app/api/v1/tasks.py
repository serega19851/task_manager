"""
API endpoints для работы с задачами
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService, TaskNotFoundError, TaskValidationError
from app.schemas.task import (
    TaskCreate, 
    TaskUpdate, 
    TaskResponse, 
    TaskList,
    APIResponse,
    ErrorResponse
)
from app.models.task import TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency для получения TaskService"""
    repository = TaskRepository(db)
    return TaskService(repository)


@router.post(
    "/",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой задачи",
    description="Создает новую задачу с указанными параметрами"
)
async def create_task(
    task_data: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    """Создание новой задачи"""
    try:
        task = task_service.create_task(task_data)
        return APIResponse(
            success=True,
            message="Задача успешно создана",
            data=task
        )
    except TaskValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )


@router.get(
    "/{task_id}",
    response_model=APIResponse,
    summary="Получение задачи по ID",
    description="Возвращает задачу с указанным идентификатором"
)
async def get_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    """Получение задачи по ID"""
    try:
        task = task_service.get_task(task_id)
        return APIResponse(
            success=True,
            message="Задача найдена",
            data=task
        )
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )


@router.get(
    "/",
    response_model=APIResponse,
    summary="Получение списка задач",
    description="Возвращает список всех задач с возможностью фильтрации по статусу"
)
async def get_tasks(
    task_status: Optional[TaskStatus] = Query(None, description="Фильтр по статусу"),
    limit: int = Query(100, ge=1, le=1000, description="Количество задач на странице"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    task_service: TaskService = Depends(get_task_service)
):
    """Получение списка задач"""
    try:
        tasks = task_service.get_tasks(status=task_status, limit=limit, offset=offset)
        return APIResponse(
            success=True,
            message=f"Найдено {tasks.total} задач",
            data=tasks
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )


@router.put(
    "/{task_id}",
    response_model=APIResponse,
    summary="Обновление задачи",
    description="Обновляет существующую задачу"
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """Обновление задачи"""
    try:
        task = task_service.update_task(task_id, task_data)
        return APIResponse(
            success=True,
            message="Задача успешно обновлена",
            data=task
        )
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TaskValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление задачи",
    description="Удаляет задачу с указанным идентификатором"
)
async def delete_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    """Удаление задачи"""
    try:
        success = task_service.delete_task(task_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с ID {task_id} не найдена"
            )
        return None  # 204 No Content
        
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except TaskValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
