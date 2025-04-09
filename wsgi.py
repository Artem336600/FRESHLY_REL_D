from app import app, initialize_clients
import os
from whitenoise import WhiteNoise

# Инициализируем клиентов при запуске сервера
initialize_clients()

# Настройка для обслуживания статических файлов через WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app)
app.wsgi_app.add_files('static/', prefix='static/')

# Получение порта из переменной окружения для Railway
try:
    port_str = os.environ.get("PORT", "5000")
    if port_str == "$PORT":  # Если переменная не заменилась
        port = 5000
    else:
        port = int(port_str)
except ValueError:
    port = 5000

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port) 