"""
Общая конфигурация для всех тестов
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override для тестовой базы данных"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Переопределяем зависимость для всех тестов
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def setup_database():
    """Фикстура для создания и очистки тестовой базы данных"""
    # Создаем таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    yield
    # Очищаем таблицы после теста
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def clean_database():
    """Фикстура для очистки базы данных после теста"""
    yield
    # Очищаем данные после теста
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """Фикстура для тестового клиента"""
    return TestClient(app)
