#!/bin/bash

# Вывод версий для отладки
echo "Python версия:"
python --version
echo "Текущая директория: $(pwd)"
echo "Содержимое директории:"
ls -la

# Экологические переменные
echo "Переменные окружения (без секретов):"
env | grep -v "KEY\|TOKEN\|PASSWORD"

# Установка зависимостей
echo "Установка минимальных зависимостей..."
pip install flask gunicorn

# Проверка, что app_railway.py существует
if [ ! -f "app_railway.py" ]; then
  echo "ОШИБКА: app_railway.py не найден!"
  ls -la
  exit 1
fi

# Проверка, что wsgi_railway.py существует
if [ ! -f "wsgi_railway.py" ]; then
  echo "ОШИБКА: wsgi_railway.py не найден!"
  ls -la
  exit 1
fi

# Определение порта из переменной окружения или использование порта по умолчанию
PORT=${PORT:-8000}
echo "Использую порт: $PORT"

# Запуск минимального приложения c явной привязкой к порту
echo "Запуск минимального приложения..."
exec gunicorn --bind=0.0.0.0:$PORT --log-level=debug wsgi_railway:app 