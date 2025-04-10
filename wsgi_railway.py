from app_railway import app
import logging

logger = logging.getLogger(__name__)

# Логирование при импорте WSGI файла
logger.info("WSGI Railway приложение инициализировано")

if __name__ == "__main__":
    logger.info("Запуск WSGI Railway приложения")
    app.run() 