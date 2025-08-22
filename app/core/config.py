"""
Конфигурация приложения Task Manager
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Информация о приложении
    app_name: str = "Task Manager API"
    version: str = "1.0.0"
    debug: bool = False
    
    # База данных
    database_url: str = "sqlite:///./data/tasks.db"
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    # Логирование
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Создание глобального экземпляра настроек
settings = Settings()
