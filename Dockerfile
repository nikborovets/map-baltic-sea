# Используем официальный Python образ
FROM python:3.11-slim

# Установим рабочую директорию в контейнере
WORKDIR /app

# Скопируем файл с зависимостями в контейнер
COPY requirements.txt requirements.txt

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем всё содержимое в контейнер
COPY . .

# Запуск через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8883", "--workers", "3", "flask_server:app"]
