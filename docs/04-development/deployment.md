# Deployment

## Общий подход

Развёртывание ЦОС «Пифагор» должно быть предсказуемым и воспроизводимым.

Для локальной разработки используется Docker Compose. Для production в будущем можно использовать VPS, облако или контейнерную инфраструктуру.

---

## Локальное окружение

Сервисы:

```text
frontend
backend
postgres
redis
celery
celery-beat
nginx
```

---

## Переменные окружения

Файл `.env.example` должен содержать пример:

```text
DEBUG=true
SECRET_KEY=change-me
DATABASE_URL=postgres://pifagor:pifagor@postgres:5432/pifagor
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

---

## Production окружение

Минимальный production-набор: backend Django, frontend build, PostgreSQL, Redis, Celery worker, Celery beat, Nginx, HTTPS, backups.

---

## Backup

Нужно регулярно сохранять базу данных, media-файлы, конфигурации и важные документы.

Минимально: daily database backup, weekly full backup, monthly archive backup.

---

## Безопасность

Production должен иметь `DEBUG=false`, сильный `SECRET_KEY`, HTTPS, ограниченный доступ к admin, закрытые порты БД, регулярные обновления, резервные копии и защиту персональных данных.

---

## Главный принцип

> Деплой должен быть повторяемым: если сервер потерян, проект можно поднять заново по документации.
