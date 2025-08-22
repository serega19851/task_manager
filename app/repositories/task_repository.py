"""
Repository для работы с задачами
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from uuid import UUID

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    """Repository для работы с задачами"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, task_data: TaskCreate) -> Task:
        """Создание новой задачи"""
        try:
            db_task = Task(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status
            )
            
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            
            return db_task
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Ошибка создания задачи: {str(e)}")
    
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Получение задачи по ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_all(self, status: Optional[TaskStatus] = None, limit: int = 100, offset: int = 0) -> List[Task]:
        """Получение списка всех задач с опциональной фильтрацией"""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        
        return query.offset(offset).limit(limit).all()
    
    def get_count(self, status: Optional[TaskStatus] = None) -> int:
        """Получение количества задач"""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        
        return query.count()
    
    def update(self, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
        """Обновление задачи"""
        try:
            db_task = self.get_by_id(task_id)
            
            if not db_task:
                return None
            
            # Обновляем только переданные поля
            update_data = task_data.model_dump(exclude_unset=True)
            
            for field, value in update_data.items():
                setattr(db_task, field, value)
            
            self.db.commit()
            self.db.refresh(db_task)
            
            return db_task
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Ошибка обновления задачи: {str(e)}")
    
    def delete(self, task_id: UUID) -> bool:
        """Удаление задачи"""
        try:
            db_task = self.get_by_id(task_id)
            
            if not db_task:
                return False
            
            self.db.delete(db_task)
            self.db.commit()
            
            return True
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Ошибка удаления задачи: {str(e)}")
    
    def exists(self, task_id: UUID) -> bool:
        """Проверка существования задачи"""
        return self.db.query(Task).filter(Task.id == task_id).first() is not None
