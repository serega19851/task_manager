"""
Тесты для API endpoints Task Manager
Проверка основных endpoint'ов, документации и обработки ошибок
"""

import pytest
import httpx
from app.models.task import TaskStatus
import json

class TestAPIEndpoints:
    """Тестовый класс для проверки основных API endpoints"""
    
    def test_root_endpoint(self, client):
        """Тест корневого endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "Task Manager API" in data["message"]
        assert data["status"] == "working"
        assert "timestamp" in data
        
    def test_health_check_endpoint(self, client):
        """Тест health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "task-manager-api"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        
    def test_swagger_docs_available(self, client):
        """Тест доступности Swagger документации"""
        response = client.get("/docs")
        assert response.status_code == 200
        
    def test_redoc_docs_available(self, client):
        """Тест доступности ReDoc документации"""
        response = client.get("/redoc")
        assert response.status_code == 200
        
    def test_openapi_schema_available(self, client):
        """Тест доступности OpenAPI схемы"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Task Manager API"
        
    def test_tasks_endpoint_empty_list(self, client, setup_database):
        """Тест endpoint задач с пустым списком"""
        response = client.get("/api/v1/tasks")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "success" in data
        assert data["success"] is True
        assert "message" in data
        assert "data" in data
        assert data["data"]["total"] == 0
        assert data["data"]["tasks"] == []

class TestAPIErrorHandling:
    """Тесты обработки ошибок"""
    
    def test_404_endpoint(self, client):
        """Тест несуществующего endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_async_http_client():
    """Тест асинхронного HTTP клиента для будущих тестов"""
    from app.main import app
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

def test_api_response_headers(client):
    """Тест заголовков ответа API"""
    response = client.get("/")
    
    # Проверяем что FastAPI устанавливает правильные заголовки
    assert "application/json" in response.headers.get("content-type", "")

if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])
