# Переменные окружения

## Общие правила

Не коммитьте `.env` с реальными секретами. Для примеров используйте `.env.example` или документацию с безопасными значениями-заглушками.

## Backend

| Переменная | Назначение | Пример |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | Настройки Django | `config.settings.local` |
| `SECRET_KEY` | Секрет Django | `change-me` |
| `DEBUG` | Режим отладки | `true` |
| `DATABASE_URL` | Подключение к PostgreSQL | `postgres://user:pass@localhost:5432/db` |
| `REDIS_URL` | Подключение к Redis | `redis://localhost:6379/0` |
| `EMAIL_HOST` | SMTP host | `smtp.example.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | SMTP user | `user@example.com` |
| `EMAIL_HOST_PASSWORD` | SMTP password | `secret` |
| `DADATA_API_KEY` | API key DaData | `secret` |

## Frontend

| Переменная | Назначение | Пример |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Базовый URL backend API | `http://localhost:8000` |
| `VITE_APP_NAME` | Название приложения | `Пифагор` |

## CI/CD

Секреты GitHub Actions должны храниться в GitHub Secrets. Не дублируйте реальные значения в workflow-файлах.
