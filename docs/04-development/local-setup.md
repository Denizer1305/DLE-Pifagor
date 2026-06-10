# Локальный запуск

## Требования

- Node.js 20.19+ или 22.12+;
- Python 3.12+;
- PostgreSQL;
- Redis;
- Git.

## Frontend

```sh
cd frontend
npm install
npm run dev
```

Проверки:

```sh
npm run type-check
npm run build
```

## Backend

```sh
cd backend
python -m venv .venv
.venv/bin/python -m pip install -r requirements/local.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Для Windows PowerShell путь к Python внутри venv может отличаться:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

## Celery и Redis

Redis должен быть запущен до старта фоновых задач. Celery используется для email, уведомлений и фоновой обработки.

## Первичная проверка

После запуска проверьте:

- публичные страницы открываются;
- вход работает;
- refresh token не разлогинивает пользователя после обновления страницы;
- личные кабинеты доступны согласно роли;
- Swagger/ReDoc открываются, если включены в окружении.
