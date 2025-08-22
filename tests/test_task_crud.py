"""
Comprehensive CRUD тесты для Task Manager API
Полное покрытие всех операций с задачами
"""

import pytest
from app.models.task import TaskStatus
import uuid
import json


class TestTaskCRUD:
    """Класс для тестирования CRUD операций с задачами"""

    def test_create_task_success(self, client, setup_database, clean_database):
        """Тест успешного создания задачи"""
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["title"] == task_data["title"]
        assert data["data"]["description"] == task_data["description"]
        assert data["data"]["status"] == TaskStatus.CREATED.value
        assert "id" in data["data"]
        
    def test_create_task_without_description(self, client, setup_database, clean_database):
        """Тест создания задачи без описания"""
        task_data = {
            "title": "Задача без описания"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["title"] == task_data["title"]
        assert data["data"]["description"] is None
        assert data["data"]["status"] == TaskStatus.CREATED.value
