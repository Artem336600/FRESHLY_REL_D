import requests
import json
import os
from dotenv import load_dotenv
import sys

# Загрузка переменных окружения
load_dotenv()

# URL для тестирования (по умолчанию локальный)
BASE_URL = os.getenv('TEST_API_URL', 'http://localhost:5000')

def test_api():
    print(f"Тестирование API по адресу: {BASE_URL}")
    
    # Проверка доступности сервера
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Сервер доступен и отвечает на запросы")
        else:
            print(f"❌ Ошибка сервера: код {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Не удалось соединиться с сервером: {e}")
        return False
    
    # Проверка API запроса
    try:
        test_data = {"text": "Яблоки"}
        response = requests.post(
            f"{BASE_URL}/process",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"❌ API вернул ошибку: {data['error']}")
                return False
            
            print("✅ API успешно обработал запрос")
            print(f"  - Тема: {data.get('topic')}")
            print(f"  - Факты: {'Получены' if data.get('facts') else 'Отсутствуют'}")
            print(f"  - Продукты: {len(data.get('products', []))} категорий")
            return True
        else:
            print(f"❌ Ошибка API: код {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании API: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1) 