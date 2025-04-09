#!/bin/bash

# Активация виртуального окружения (если используется)
# source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск через Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 4 --timeout 120 