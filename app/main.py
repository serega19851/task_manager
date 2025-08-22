"""
Task Manager API - Полноценное FastAPI приложение
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import structlog

from app.core.config import settings
from app.core.database import create_tables
from app.api.v1.tasks import router as tasks_router
from app.services.task_service import TaskNotFoundError, TaskValidationError

# Настройка логирования
logger = structlog.get_logger()

# Создание FastAPI приложения
app = FastAPI(
    title=settings.app_name,
    description="REST API для управления задачами с полным функционалом CRUD",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(tasks_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    logger.info("Запуск Task Manager API")
    create_tables()
    logger.info("Таблицы базы данных созданы")


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    """Обработчик исключения TaskNotFoundError"""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "TASK_NOT_FOUND",
            "message": str(exc)
        }
    )


@app.exception_handler(TaskValidationError)
async def task_validation_handler(request: Request, exc: TaskValidationError):
    """Обработчик исключения TaskValidationError"""
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": str(exc)
        }
    )


@app.get("/")
async def root():
    """Корневой endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Task Manager API",
        "status": "working",
        "version": settings.version,
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs",
        "api": {
            "v1": settings.api_v1_prefix,
            "endpoints": [
                "POST /api/v1/tasks - создание задачи",
                "GET /api/v1/tasks - список задач",
                "GET /api/v1/tasks/{id} - задача по ID", 
                "PUT /api/v1/tasks/{id} - обновление задачи",
                "DELETE /api/v1/tasks/{id} - удаление задачи"
            ]
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "task-manager-api",
        "version": settings.version,
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level=settings.log_level.lower()
    )
