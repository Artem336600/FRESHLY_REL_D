from flask import Flask, jsonify
import logging
import os

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
        "status": "healthy",
        "service": "Freshly API",
        "version": "1.0.0"
    })

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
    return jsonify({
        "status": "error",
        "message": f"Внутренняя ошибка сервера: {str(e)}"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Запуск приложения на порту {port}")
    app.run(host='0.0.0.0', port=port) 