"""
Модель задачи для Task Manager
"""

from sqlalchemy import Column, String, Text, DateTime, Enum, TypeDecorator
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's UUID type when available, otherwise String(36).
    """
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value


class TaskStatus(str, enum.Enum):
    """Task statuses"""
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    """Модель задачи"""
    
    __tablename__ = "tasks"
    
    # Основные поля
    id = Column(
        GUID(), 
        primary_key=True, 
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    
    title = Column(
        String(255), 
        nullable=False,
        comment="Название задачи"
    )
    
    description = Column(
        Text, 
        nullable=True,
        comment="Описание задачи"
    )
    
    status = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.CREATED,
        comment="Статус задачи"
    )
    
    # Временные метки
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Дата создания"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Дата последнего обновления"
    )
    
    def __repr__(self):
        """Строковое представление модели"""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"
    
    def __str__(self):
        """Удобочитаемое представление"""
        return f"Задача: {self.title} ({self.status.value})"
