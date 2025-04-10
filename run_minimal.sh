#!/bin/bash

# Create a very simple Flask test app
echo "Creating extremely simple test app..."
cat > test_app.py << 'EOF'
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Railway!"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
EOF

# Экологические переменные
echo "Переменные окружения (без секретов):"
env | grep -v "KEY\|TOKEN\|PASSWORD"

# Установка зависимостей
echo "Установка минимальных зависимостей..."
pip install flask gunicorn

# Определение порта из переменной окружения или использование порта по умолчанию
PORT=${PORT:-8000}
echo "Использую порт: $PORT"

# Запуск минимального тестового приложения с явной привязкой к порту
echo "Запуск минимального тестового приложения..."
exec gunicorn --workers=1 --log-level=debug --bind="0.0.0.0:$PORT" "test_app:app" 