from app import app, initialize_clients
import os
from whitenoise import WhiteNoise
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Проверка наличия переменных окружения
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY")
deepseek_base_url = os.environ.get("DEEPSEEK_BASE_URL")

# Вывод отладочной информации (будет в логах Railway)
print(f"SUPABASE_URL задан: {'Да' if supabase_url else 'Нет'}")
print(f"SUPABASE_KEY задан: {'Да' if supabase_key else 'Нет'}")
print(f"DEEPSEEK_API_KEY задан: {'Да' if deepseek_api_key else 'Нет'}")
print(f"DEEPSEEK_BASE_URL задан: {'Да' if deepseek_base_url else 'Нет'}")

# Устанавливаем значения напрямую, если они не заданы в переменных окружения
if not supabase_url:
    os.environ["SUPABASE_URL"] = "https://rgyhaiaecqusymobdqdd.supabase.co"
    print("SUPABASE_URL установлен принудительно")
    
if not supabase_key:
    os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJneWhhaWFlY3F1c3ltb2JkcWRkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODI0NjkyOCwiZXhwIjoyMDUzODIyOTI4fQ.oZe5DEPVuSCAzeKZxLInsF8iJWXBEGS9I9H6gGMBlmc"
    print("SUPABASE_KEY установлен принудительно")
    
if not deepseek_api_key:
    os.environ["DEEPSEEK_API_KEY"] = "sk-4343a8699fd7460d98903b12836a4627"
    print("DEEPSEEK_API_KEY установлен принудительно")
    
if not deepseek_base_url:
    os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com"
    print("DEEPSEEK_BASE_URL установлен принудительно")

if not os.environ.get("DEEPSEEK_MODEL"):
    os.environ["DEEPSEEK_MODEL"] = "deepseek-chat"
    print("DEEPSEEK_MODEL установлен принудительно")

# Инициализируем клиентов при запуске сервера
success = initialize_clients()
if not success:
    print("КРИТИЧЕСКАЯ ОШИБКА: Не удалось инициализировать клиентов даже после принудительной установки переменных окружения")
else:
    print("Клиенты успешно инициализированы")

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