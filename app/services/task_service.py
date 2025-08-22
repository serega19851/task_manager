"""
Сервис для работы с задачами (бизнес-логика)
"""

from typing import List, Optional
from uuid import UUID
import structlog

from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskList
from app.models.task import TaskStatus

logger = structlog.get_logger()


class TaskNotFoundError(Exception):
    """Исключение когда задача не найдена"""
    pass


class TaskValidationError(Exception):
    """Исключение валидации задачи"""
    pass


class TaskService:
    """Сервис для работы с задачами"""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Создание новой задачи"""
        try:
            # Валидация данных
            if not task_data.title or not task_data.title.strip():
                raise TaskValidationError("Название задачи не может быть пустым")
            
            # Создание задачи через repository
            db_task = self.repository.create(task_data)
            
            logger.info("Задача создана", task_id=str(db_task.id), title=task_data.title)
            
            return TaskResponse.model_validate(db_task)
            
        except ValueError as e:
            logger.error("Ошибка создания задачи", error=str(e))
            raise TaskValidationError(str(e))
    
    def get_task(self, task_id: UUID) -> TaskResponse:
        """Получение задачи по ID"""
        db_task = self.repository.get_by_id(task_id)
        
        if not db_task:
            logger.warning("Задача не найдена", task_id=str(task_id))
            raise TaskNotFoundError(f"Задача с ID {task_id} не найдена")
        
        logger.info("Задача получена", task_id=str(task_id))
        return TaskResponse.model_validate(db_task)
    
    def get_tasks(
        self, 
        status: Optional[TaskStatus] = None, 
        limit: int = 100, 
        offset: int = 0
    ) -> TaskList:
        """Получение списка задач"""
        db_tasks = self.repository.get_all(status=status, limit=limit, offset=offset)
        total = self.repository.get_count(status=status)
        
        tasks = [TaskResponse.model_validate(task) for task in db_tasks]
        
        logger.info(
            "Список задач получен", 
            count=len(tasks), 
            total=total, 
            status=status.value if status else None
        )
        
        return TaskList(tasks=tasks, total=total)
    
    def update_task(self, task_id: UUID, task_data: TaskUpdate) -> TaskResponse:
        """Обновление задачи"""
        try:
            # Проверяем существование задачи
            if not self.repository.exists(task_id):
                raise TaskNotFoundError(f"Задача с ID {task_id} не найдена")
            
            # Валидация данных
            if task_data.title is not None and (not task_data.title or not task_data.title.strip()):
                raise TaskValidationError("Название задачи не может быть пустым")
            
            # Обновление через repository
            db_task = self.repository.update(task_id, task_data)
            
            if not db_task:
                raise TaskNotFoundError(f"Задача с ID {task_id} не найдена")
            
            logger.info("Задача обновлена", task_id=str(task_id))
            
            return TaskResponse.model_validate(db_task)
            
        except ValueError as e:
            logger.error("Ошибка обновления задачи", task_id=str(task_id), error=str(e))
            raise TaskValidationError(str(e))
    
    def delete_task(self, task_id: UUID) -> bool:
        """Удаление задачи"""
        try:
            # Проверяем существование задачи
            if not self.repository.exists(task_id):
                raise TaskNotFoundError(f"Задача с ID {task_id} не найдена")
            
            success = self.repository.delete(task_id)
            
            if success:
                logger.info("Задача удалена", task_id=str(task_id))
            else:
                logger.error("Не удалось удалить задачу", task_id=str(task_id))
            
            return success
            
        except ValueError as e:
            logger.error("Ошибка удаления задачи", task_id=str(task_id), error=str(e))
            raise TaskValidationError(str(e))
    
    def get_tasks_by_status(self, status: TaskStatus) -> TaskList:
        """Получение задач по статусу"""
        return self.get_tasks(status=status)
    
    def change_task_status(self, task_id: UUID, new_status: TaskStatus) -> TaskResponse:
        """Изменение статуса задачи"""
        task_update = TaskUpdate(status=new_status)
        return self.update_task(task_id, task_update)
