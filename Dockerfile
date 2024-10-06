FROM python:3.12-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем netcat для проверки доступности базы данных
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY . .