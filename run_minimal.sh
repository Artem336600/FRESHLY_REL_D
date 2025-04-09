#!/bin/bash

# Вывод версий для отладки
echo "Python версия:"
python --version
echo "Текущая директория: $(pwd)"
echo "Содержимое директории:"
ls -la

# Установка зависимостей
echo "Установка минимальных зависимостей..."
pip install flask gunicorn

# Запуск минимального приложения
echo "Запуск минимального приложения..."
gunicorn wsgi_railway:app 