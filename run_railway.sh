#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Запуск через Gunicorn без явного указания порта
# Railway автоматически передаст переменную PORT в окружение
gunicorn wsgi:app 