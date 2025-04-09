# Freshly - Анализ продуктов питания

Приложение для поиска продуктов по различным темам с использованием ИИ.

## Требования

- Python 3.8+
- Учетные записи Supabase и DeepSeek AI

## Установка

1. Клонировать репозиторий
2. Установить зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Настроить переменные окружения, создав файл `.env` со следующими параметрами:
   ```
   SUPABASE_URL=ваш_url
   SUPABASE_KEY=ваш_ключ
   DEEPSEEK_API_KEY=ваш_ключ
   DEEPSEEK_BASE_URL=https://api.deepseek.com
   DEEPSEEK_MODEL=deepseek-chat
   ```

## Локальный запуск

### Консольный режим
```
python app.py
```

### Веб-режим
```
python app.py --web
```

## Деплой на сервер

### Вариант 1: Railway (рекомендуется)
1. Зарегистрируйтесь на [Railway](https://railway.app/)
2. Создайте новый проект, выбрав опцию "Deploy from GitHub repo"
3. Подключите свой GitHub репозиторий
4. Настройте переменные окружения в разделе "Variables"
5. Нажмите "Deploy"

Подробные инструкции смотрите в файле [RAILWAY.md](RAILWAY.md)

### Вариант 2: Heroku
1. Создайте приложение на Heroku
2. Настройте переменные окружения в настройках Heroku
3. Разверните приложение через Git:
   ```
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a имя-вашего-приложения
   git push heroku master
   ```

### Вариант 3: VPS с Gunicorn и Nginx
1. Перенесите код на сервер
2. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Запустите с помощью Gunicorn:
   ```
   gunicorn wsgi:app -b 0.0.0.0:8000
   ```
4. Настройте Nginx для проксирования на порт 8000

### Вариант 4: Docker
1. Создайте Dockerfile в корне проекта (см. ниже)
2. Соберите и запустите Docker-образ:
   ```
   docker build -t freshly .
   docker run -p 5000:5000 --env-file .env freshly
   ```

## Dockerfile
Пример Dockerfile для проекта:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
``` 