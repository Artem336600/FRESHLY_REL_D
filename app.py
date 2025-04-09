from flask import Flask, render_template, request, jsonify
import os
import re
from supabase import create_client, Client
from openai import OpenAI
import textwrap
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

app = Flask(__name__)

# --- Конфигурация Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "Products"
SEARCH_COLUMN = "product"
ID_COLUMN = "id"
IMG_COLUMN = "img"
COST_COLUMN = "cost"
AVAILABILITY_COLUMN = "availability"
CATEGORY_COLUMN = "category"

# --- Конфигурация DeepSeek ---
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# --- Инициализация клиентов ---
supabase = None
deepseek_client = None

def initialize_clients():
    global supabase, deepseek_client
    try:
        print(f"Попытка инициализации клиентов со следующими параметрами:")
        print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
        print(f"SUPABASE_KEY: {os.getenv('SUPABASE_KEY')[:10]}... (скрыто)")
        print(f"DEEPSEEK_API_KEY: {os.getenv('DEEPSEEK_API_KEY')[:10]}... (скрыто)")
        print(f"DEEPSEEK_BASE_URL: {os.getenv('DEEPSEEK_BASE_URL')}")
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Клиент Supabase инициализирован успешно")
        
        deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        print("Клиент DeepSeek инициализирован успешно")
        
        print("Успешная инициализация всех клиентов.")
        return True
    except Exception as e:
        print(f"Ошибка инициализации клиентов: {e}")
        return False

# --- Вспомогательные функции ---
def print_product_info(item):
    """Аккуратно выводит информацию о продукте."""
    try:
        product_name = item.get(SEARCH_COLUMN, 'Название не найдено')
        cost = item.get(COST_COLUMN, 'Цена не указана')
        image_url = item.get(IMG_COLUMN, 'https://via.placeholder.com/300x200?text=Нет+изображения')
        availability = item.get(AVAILABILITY_COLUMN, '?')
        category = item.get(CATEGORY_COLUMN, '?')

        # Проверка и исправление URL изображения
        if image_url and not image_url.startswith(('http://', 'https://')):
            image_url = 'https://via.placeholder.com/300x200?text=Некорректная+ссылка'
        elif image_url == 'Нет URL изображения':
            image_url = 'https://via.placeholder.com/300x200?text=Нет+изображения'

        info = f"    - Продукт: {product_name}\n"
        info += f"      Стоимость: {cost}\n"
        if availability != '?': info += f"      Наличие: {availability}\n"
        if category != '?': info += f"      Категория БД: {category}\n"
        info += f"      Изображение: {image_url}\n"
        info += "      " + "-" * 15 + "\n"
        return info
    except Exception as e:
        return f"    Ошибка при обработке записи {item.get(SEARCH_COLUMN, 'ID: ' + str(item.get(ID_COLUMN)))}: {e}\n"

def normalize_string(text: str) -> str:
    """Приводит строку к нижнему регистру и удаляет небуквенно-цифровые символы, кроме пробелов."""
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    return ' '.join(cleaned.lower().split())

def get_facts_and_explained_food(topic):
    """Отправляет запрос к DeepSeek для генерации фактов о теме."""
    if not deepseek_client:
        return "Ошибка: Клиент DeepSeek не инициализирован."

    prompt = f"""
Пожалуйста, сгенерируй 5-7 интересных и разнообразных фактов о теме: "{topic}". Представь их в виде нумерованного списка.

После списка фактов, отдельной строкой, перечисли в скобках несколько (3-5) **распространенных, широко доступных** продуктов питания, напитков, готовых блюд или основных ингредиентов.
**ВАЖНО:**
1.  Для каждого продукта **сразу после него через двоеточие (:) укажи КРАТКОЕ объяснение (1-2 предложения), почему этот продукт связан с темой "{topic}"**.
2.  **КРАЙНЕ ВАЖНО: Если продукт - это фрукт, овощ или другой исчисляемый предмет (например, яблоко, огурец, пряник, орех, лимон), ВСЕГДА используй МНОЖЕСТВЕННОЕ ЧИСЛО (Яблоки, Огурцы, Пряники, Орехи, Лимоны), даже если в разговорной речи чаще используется единственное. Для неисчисляемых (сахар, мука, вода) или общих категорий (выпечка, суп) используй единственное число или общее название.**
3.  Выводи только реальные продукты, ничего лишнего. Если упоминается сочетание (например, чай с мёдом), предложи основные компоненты отдельно (Чай, Мёд).

**Формат вывода списка продуктов:** `(Продукт1: Краткое объяснение связи1, Продукт2: Краткое объяснение связи2, ...)`
"""

    messages = [
        {"role": "system", "content": "Ты — эрудированный ассистент, который находит реальные продукты питания, связанные с темой."},
        {"role": "user", "content": prompt},
    ]

    try:
        response = deepseek_client.chat.completions.create(
            model=DEEPSEEK_MODEL, messages=messages, stream=False, max_tokens=800,
            temperature=0.65
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка API DeepSeek: {e}"

def extract_food_items_with_reasons(text: str) -> list[dict]:
    """Извлекает список продуктов и их объяснений из строки."""
    items_with_reasons = []
    match = re.search(r'\(([^)]*)\)[^)]*$', text)
    if match:
        content = match.group(1).strip()
        pattern = r'(\S[^:]*?):\s*(.*?)(?=(?:,\s*\S[^:]*?:)|$)'
        matches = re.findall(pattern, content)

        if matches:
            for item, reason in matches:
                item = item.strip()
                reason = reason.strip().rstrip(',')
                if item and reason:
                    items_with_reasons.append({'item': item, 'reason': reason})
    return items_with_reasons

def extract_facts(text: str) -> str:
    """Извлекает факты (текст до скобок с продуктами)."""
    match = re.search(r'\(([^)]*)\)[^)]*$', text)
    if match:
        facts_part = text[:match.start()].strip()
        return '\n'.join(line for line in facts_part.splitlines() if line.strip())
    return text.strip()

def find_products_for_keyword(keyword: str):
    """Ищет продукты по ключевому слову."""
    if not supabase: return []
    if not keyword: return []
    normalized_keyword = normalize_string(keyword)
    if not normalized_keyword: return []

    try:
        response = supabase.table(TABLE_NAME) \
            .select('*') \
            .ilike(SEARCH_COLUMN, f'%{normalized_keyword}%') \
            .execute()

        if response.data:
            return sorted(response.data, key=lambda x: normalize_string(x.get(SEARCH_COLUMN, "")))
        return []
    except Exception as e:
        print(f"Ошибка поиска в Supabase: {e}")
        return []

def process_topic(topic: str) -> dict:
    """Обрабатывает тему и возвращает результаты в виде словаря."""
    if not topic:
        return {"error": "Тема не была введена."}

    deepseek_result_text = get_facts_and_explained_food(topic)
    if "Ошибка API DeepSeek" in deepseek_result_text:
        return {"error": deepseek_result_text}

    explanation_facts = extract_facts(deepseek_result_text)
    food_items_data = extract_food_items_with_reasons(deepseek_result_text)

    results = {
        "topic": topic,
        "facts": explanation_facts,
        "products": []
    }

    for item_data in food_items_data:
        keyword = item_data['item']
        reason = item_data['reason']
        specific_products = find_products_for_keyword(keyword)

        if specific_products:
            products_info = []
            for product in specific_products:
                products_info.append(print_product_info(product))

            results["products"].append({
                "category": keyword,
                "reason": reason,
                "items": products_info
            })

    return results

# --- Веб-маршруты ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if not supabase or not deepseek_client:
        if not initialize_clients():
            return jsonify({"error": "Ошибка: Не удалось инициализировать клиенты. Проверьте подключение к интернету и API ключи."})
    
    data = request.json
    topic = data.get('text', '').strip()
    results = process_topic(topic)
    return jsonify(results)

# --- Консольный режим ---
def console_mode():
    if not initialize_clients():
        return

    try:
        while True:
            user_topic = input("\nВведите тему для поиска (или 'выход' для завершения): ").strip()
            if user_topic.lower() == 'выход':
                break

            results = process_topic(user_topic)
            
            if "error" in results:
                print(f"\nОшибка: {results['error']}")
                continue

            print("\n" + "="*50)
            print(f"РЕЗУЛЬТАТЫ ПО ТЕМЕ: {results['topic'].upper()}")
            print("="*50)

            if results['facts']:
                print("\n--- Общая информация по теме (от ИИ) ---")
                print(textwrap.fill(results['facts'], width=80, initial_indent="  ", subsequent_indent="  "))

            if results['products']:
                print("\n--- Связанные продукты в базе данных ---")
                for category in results['products']:
                    print(f"\n=== {category['category'].upper()} ===")
                    print("   " + "-"*30)
                    print(f"   Объяснение связи (от ИИ):")
                    print(textwrap.fill(category['reason'], width=75, initial_indent="     ", subsequent_indent="     "))
                    print("   " + "-"*30)
                    print("   Найденные товары в базе:")
                    for item in category['items']:
                        print(item)
            else:
                print("\nНе найдено продуктов в базе данных.")

    except KeyboardInterrupt:
        print("\nВыход из программы по команде пользователя.")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        if not initialize_clients():
            print("Ошибка: Не удалось инициализировать клиенты. Проверьте подключение к интернету и API ключи.")
            sys.exit(1)
        try:
            port_str = os.environ.get("PORT", "5000")
            if port_str == "$PORT":  # Если переменная не заменилась
                port = 5000
            else:
                port = int(port_str)
        except ValueError:
            port = 5000
        app.run(debug=(os.environ.get('FLASK_DEBUG', 'False') == 'True'), 
                host='0.0.0.0', 
                port=port)
    else:
        console_mode()