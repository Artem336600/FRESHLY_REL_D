from flask import Flask, jsonify
import logging
import os
import sys

# Настройка логирования на стандартный вывод
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Инициализация приложения Railway")

# Создание приложения
app = Flask(__name__)
logger.info("Flask приложение создано")

@app.route('/')
def index():
    logger.info("Запрос к корневому маршруту '/'")
    return jsonify({
        "status": "ok",
        "message": "Freshly API работает"
    })

@app.route('/health')
def health():
    logger.info("Запрос к маршруту '/health'")
    return jsonify({
        "status": "healthy"
    })

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
    return jsonify({
        "status": "error",
        "message": f"Внутренняя ошибка сервера: {str(e)}"
    }), 500

# Отладочная информация
logger.info(f"Переменные окружения (без секретов): {[k for k in os.environ.keys() if not any(s in k.lower() for s in ['key', 'token', 'secret', 'password'])]}")
logger.info(f"Порт: {os.environ.get('PORT', '(не задан)')}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Запуск приложения на порту {port}")
    app.run(host='0.0.0.0', port=port) 