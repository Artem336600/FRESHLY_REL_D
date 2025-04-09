# Деплой на Railway

## Шаги для деплоя приложения Freshly на Railway

### 1. Создание аккаунта и проекта

1. Зарегистрируйтесь на [Railway](https://railway.app/)
2. Создайте новый проект, выбрав опцию "Deploy from GitHub repo"
3. Подключите свой GitHub репозиторий FRESHLY_REL_D

### 2. Настройка переменных окружения

В разделе "Variables" добавьте следующие переменные окружения:

```
FLASK_APP=app.py
FLASK_ENV=production
FLASK_DEBUG=False
SUPABASE_URL=https://rgyhaiaecqusymobdqdd.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJneWhhaWFlY3F1c3ltb2JkcWRkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODI0NjkyOCwiZXhwIjoyMDUzODIyOTI4fQ.oZe5DEPVuSCAzeKZxLInsF8iJWXBEGS9I9H6gGMBlmc
DEEPSEEK_API_KEY=sk-4343a8699fd7460d98903b12836a4627
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

> Примечание: Рекомендуется обновить API ключи после завершения разработки для повышения безопасности.

### 3. Настройка сервиса

1. Railway автоматически определит, что это Python-приложение
2. В настройках проекта убедитесь, что указан правильный порт в переменной `PORT` (обычно Railway делает это автоматически)
3. Нажмите "Deploy" для запуска процесса развертывания

### 4. Мониторинг деплоя

1. Следите за логами в разделе "Deployments"
2. Проверьте, что все этапы сборки прошли успешно
3. После успешного деплоя, приложение будет доступно по URL, указанному в разделе "Settings"

### 5. Настройка домена (опционально)

1. В разделе "Settings" -> "Domains" вы можете настроить пользовательский домен
2. Следуйте инструкциям по добавлению DNS-записей для вашего домена

### Полезные команды Railway CLI

Вы также можете использовать Railway CLI для управления проектом:

```bash
# Установка Railway CLI
npm i -g @railway/cli

# Вход в аккаунт
railway login

# Привязка к проекту
railway link

# Деплой проекта
railway up

# Просмотр логов
railway logs

# Открыть приложение в браузере
railway open
```

### Решение проблем

Если возникли проблемы с деплоем:

1. Проверьте логи развертывания в разделе "Deployments"
2. Убедитесь, что все переменные окружения настроены правильно
3. Проверьте, что приложение правильно обрабатывает порт (PORT), назначенный Railway
4. Запустите тесты локально перед деплоем: `python test_api.py` 