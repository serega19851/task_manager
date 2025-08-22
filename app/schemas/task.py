"""
Pydantic схемы для Task Manager
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    """Базовая схема задачи"""
    
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=255,
        description="Название задачи"
    )
    
    description: Optional[str] = Field(
        None, 
        max_length=1000,
        description="Описание задачи"
    )
    
    status: TaskStatus = Field(
        default=TaskStatus.CREATED,
        description="Статус задачи"
    )


class TaskCreate(TaskBase):
    """Схема для создания задачи"""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    
    title: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=255,
        description="Название задачи"
    )
    
    description: Optional[str] = Field(
        None, 
        max_length=1000,
        description="Описание задачи"
    )
    
    status: Optional[TaskStatus] = Field(
        None,
        description="Статус задачи"
    )


class TaskResponse(TaskBase):
    """Схема для ответа с данными задачи"""
    
    id: UUID = Field(description="Уникальный идентификатор задачи")
    created_at: datetime = Field(description="Дата создания")
    updated_at: datetime = Field(description="Дата последнего обновления")
    
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    """Схема для списка задач"""
    
    tasks: list[TaskResponse] = Field(description="Список задач")
    total: int = Field(description="Общее количество задач")


class APIResponse(BaseModel):
    """Базовая схема ответа API"""
    
    success: bool = Field(description="Успешность операции")
    message: str = Field(description="Сообщение")
    data: Optional[TaskResponse | TaskList] = Field(None, description="Данные")


class ErrorResponse(BaseModel):
    """Схема для ошибок"""
    
    success: bool = Field(default=False, description="Успешность операции")
    error: str = Field(description="Код ошибки")
    message: str = Field(description="Описание ошибки")
    details: Optional[dict] = Field(None, description="Дополнительная информация")
