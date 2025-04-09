FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Переменные окружения для запуска
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Порт для приложения
EXPOSE 5000

# Запуск приложения с Gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"] 