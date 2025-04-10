import logging
import sys

# Настройка логирования до импорта приложения
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Инициализация WSGI Railway")

try:
    from app_railway import app
    logger.info("Приложение app_railway успешно импортировано")
except Exception as e:
    logger.error(f"Ошибка при импорте app_railway: {e}", exc_info=True)
    raise

# Экспорт приложения для Gunicorn
logger.info("WSGI Railway приложение успешно инициализировано")

if __name__ == "__main__":
    logger.info("Запуск WSGI Railway приложения через __main__")
    app.run() 