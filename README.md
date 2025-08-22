# Task Manager API

Современный REST API для управления задачами, созданный с использованием FastAPI.

## 🎯 Описание

Task Manager API предоставляет полный функционал CRUD операций для управления задачами.

## 🚀 Технологический стек

- **Framework**: FastAPI 0.104+
- **Database**: SQLite + SQLAlchemy 2.0+
- **Testing**: pytest 7.4+
- **Validation**: Pydantic 2.5+
- **Logging**: structlog
- **Containerization**: Docker

## 🛠️ Установка и запуск

### Требования

- Python 3.11+
- pip

### 1. Клонирование и настройка

```bash
# Перейти в директорию проекта
cd task_manager

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
# Запуск сервера разработки
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Или запуск через Python
python app/main.py
```

### 3. Доступ к API

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🐳 Docker

### Сборка и запуск

```bash
# Сборка образа
docker build -t task-manager .

# Запуск контейнера
docker run -p 8000:8000 task-manager

# Запуск с подключением локальной директории для данных
docker run -p 8000:8000 -v $(pwd)/data:/app/data task-manager
```

## 📝 API Endpoints

### Базовые endpoints

| Метод | URL       | Описание             |
| ----- | --------- | -------------------- |
| GET   | `/`       | Информация о API     |
| GET   | `/health` | Проверка состояния   |
| GET   | `/docs`   | Swagger документация |

### Endpoints для задач

| Метод  | URL                  | Описание               |
| ------ | -------------------- | ---------------------- |
| POST   | `/api/v1/tasks/`     | Создание новой задачи  |
| GET    | `/api/v1/tasks/`     | Получение списка задач |
| GET    | `/api/v1/tasks/{id}` | Получение задачи по ID |
| PUT    | `/api/v1/tasks/{id}` | Обновление задачи      |
| DELETE | `/api/v1/tasks/{id}` | Удаление задачи        |

### Модель задачи

```json
{
  "id": "uuid4",
  "title": "string (1-255 символов)",
  "description": "string (0-1000 символов, опционально)",
  "status": "created | in_progress | completed",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 💡 Примеры использования

### Создание задачи

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Изучить FastAPI",
       "description": "Прочитать документацию и создать простое приложение",
       "status": "created"
     }'
```

### Получение всех задач

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/"
```

### Получение задач по статусу

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?status=in_progress"
```

### Обновление задачи

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/{task_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "completed"
     }'
```

### Удаление задачи

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/{task_id}"
```

## 🧪 Тестирование

### Запуск всех тестов

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск с покрытием кода
python -m pytest --cov=app tests/

# Запуск конкретного файла тестов
pytest tests/test_task_crud.py -v

```

### Структура тестов

- **test_api_endpoints.py** - базовые тесты API
- **test_task_crud.py** - comprehensive CRUD тесты

## 🔧 Конфигурация

Конфигурация осуществляется через переменные окружения или файл `.env`:

```env
# База данных
DATABASE_URL=sqlite:///./data/tasks.db

# Приложение
APP_NAME="Task Manager API"
DEBUG=False
LOG_LEVEL=INFO

# API
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["*"]
```
