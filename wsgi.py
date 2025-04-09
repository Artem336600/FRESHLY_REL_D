from app import app, initialize_clients

# Инициализируем клиентов при запуске сервера
initialize_clients()

if __name__ == "__main__":
    app.run() 