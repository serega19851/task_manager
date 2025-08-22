# Multi-stage Docker build для Task Manager API
# Этап 1: Сборка зависимостей
FROM python:3.11-slim as builder

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Этап 2: Продакшн образ
FROM python:3.11-slim

WORKDIR /app

# Копирование установленных зависимостей из builder этапа
COPY --from=builder /root/.local /root/.local

# Добавление локального bin в PATH
ENV PATH=/root/.local/bin:$PATH

# Копирование requirements в production stage тоже
COPY requirements.txt /app/

# Устанавливаем все зависимости в production stage
RUN pip install --no-cache-dir -r requirements.txt

# Создание директории для данных
RUN mkdir -p /app/data

# Копирование приложения
COPY ./app /app/app

# Установка переменных окружения
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./data/tasks.db

# Открытие порта
EXPOSE 8000

# Проверка здоровья контейнера
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
