#!/bin/bash

# Вывод версий и окружения для отладки
echo "Python версия:"
python --version
echo "Pip версия:"
pip --version
echo "Текущая директория: $(pwd)"
echo "Содержимое директории:"
ls -la

# Установка зависимостей
echo "Установка зависимостей..."
pip install -r requirements.txt

# Подготовка переменных окружения
if [ ! -f .env ]; then
  echo "Файл .env не найден, копирую из .env.example"
  cp .env.example .env
fi

# Вывод содержимого .env файла для отладки (без вывода секретов)
echo "Содержимое .env файла (без секретов):"
grep -v "KEY\|TOKEN" .env | grep -v "PASSWORD"

# Экспорт переменных окружения напрямую
export SUPABASE_URL="https://rgyhaiaecqusymobdqdd.supabase.co"
export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJneWhhaWFlY3F1c3ltb2JkcWRkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODI0NjkyOCwiZXhwIjoyMDUzODIyOTI4fQ.oZe5DEPVuSCAzeKZxLInsF8iJWXBEGS9I9H6gGMBlmc"
export DEEPSEEK_API_KEY="sk-4343a8699fd7460d98903b12836a4627"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
export DEEPSEEK_MODEL="deepseek-chat"

echo "Переменные окружения экспортированы"

# Запуск через Gunicorn без явного указания порта
# Railway автоматически передаст переменную PORT в окружение
echo "Запуск приложения..."
gunicorn wsgi:app 