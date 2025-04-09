from app import app, initialize_clients
import os
from whitenoise import WhiteNoise

# Инициализируем клиентов при запуске сервера
initialize_clients()

# Настройка для обслуживания статических файлов через WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app)
app.wsgi_app.add_files('static/', prefix='static/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 