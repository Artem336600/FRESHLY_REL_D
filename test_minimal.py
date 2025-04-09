import requests
import json
import sys

def test_minimal_app(url="http://localhost:8080"):
    print(f"Тестирование минимального приложения по адресу: {url}")
    
    try:
        # Проверка основного маршрута
        print(f"Запрос к {url}...")
        response = requests.get(url, timeout=5)
        print(f"Статус ответа: {response.status_code}")
        if response.status_code == 200:
            print("Ответ:", json.dumps(response.json(), indent=2, ensure_ascii=False))
            return True
        else:
            print(f"Ошибка: Статус {response.status_code}")
            return False
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:8080"
    
    success = test_minimal_app(url)
    sys.exit(0 if success else 1) 