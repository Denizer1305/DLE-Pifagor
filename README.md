<!-- DLE-Pifagor Root Header -->
<p align="center">
  <a href="README.md"><img src="design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="docs/README.md">Документация</a> ·
  <a href="frontend/README.md">Frontend</a> ·
  <a href="backend/README.md">Backend</a> ·
  <a href="README.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor Root Header -->

## О проекте

**ЦОС "Пифагор"** - образовательная платформа, которая объединяет публичный
сайт, авторизацию, личные кабинеты администратора, преподавателя, ученика и
родителя, учебные материалы, курсы, тестирование, организации, уведомления,
обращения и настройки пользователя.

Проект ведется как монорепозиторий:

- `backend` отвечает за доменную модель, REST API, роли, права доступа,
  уведомления, фоновые задачи и обработку данных;
- `frontend` предоставляет ролевые интерфейсы на Vue 3 и TypeScript;
- `docs` хранит продуктовую, архитектурную, API и эксплуатационную
  документацию;
- `design`, `infra`, `scripts` содержат визуальные материалы, инфраструктуру и
  проектные утилиты.

## Быстрые ссылки

| Раздел | Ссылка |
| --- | --- |
| Документация проекта | `docs/README.md` |
| Структура проекта | `docs/01-architecture/project-structure.md` |
| Backend-архитектура | `docs/01-architecture/backend-architecture.md` |
| Frontend-архитектура | `docs/01-architecture/frontend-architecture.md` |
| API-архитектура | `docs/01-architecture/api-architecture.md` |
| OpenAPI | `docs/06-api/openapi.md` |
| OpenAPI snapshot | `docs/06-api/openapi.yaml` |
| Локальный запуск | `docs/04-development/local-setup.md` |
| Правила разработки | `docs/04-development/coding-rules.md` |
| Release checklist | `docs/07-operations/release-checklist.md` |

## Стек

Backend:

- Python 3.12+
- Django 5
- Django REST Framework
- drf-spectacular
- Celery и Redis
- PostgreSQL/SQLite по окружению
- Ruff, Black, isort, pytest

Frontend:

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- Font Awesome

## Реализованные области

- публичные страницы и форма обратной связи;
- авторизация, регистрация, refresh token, восстановление пароля;
- пользователи, роли, профили, настройки и безопасность;
- организации, отделения, группы, предметы, преподаватели и кураторы;
- dashboard для ролей администратора, преподавателя, ученика и родителя;
- курсы, учебные материалы и прогресс;
- тестирование: банк вопросов, тесты, попытки, ответы, проверка и результаты;
- уведомления, счетчики, прочтение и настройки доставки;
- календарь, заметки, журнал, расписание и расширяемые учебные модули;
- OpenAPI-схема и Swagger/ReDoc.

## Запуск

Из корня репозитория можно использовать `Makefile`.

```sh
make env-copy
make backend-install
make frontend-install
make backend-run
make frontend-run
```

Ручной запуск backend:

```sh
cd backend
python -m venv .venv
.venv/bin/python -m pip install -r requirements/local.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Ручной запуск frontend:

```sh
cd frontend
npm install
npm run dev
```

## Проверки

Backend:

```sh
make backend-ci
```

Frontend:

```sh
make frontend-ci
```

Полная локальная проверка с pre-commit:

```sh
make check
```

## API

Backend публикует OpenAPI через `drf-spectacular`:

- `/api/schema/` - машинно-читаемая схема;
- `/api/docs/` - Swagger UI;
- `/api/redoc/` - ReDoc.

Snapshot схемы хранится в `docs/06-api/openapi.yaml`.

## Документация

Начните с `docs/README.md`. Там собраны ссылки на видение продукта,
архитектуру, модули, дизайн-систему, правила разработки, пользовательские
инструкции, API и эксплуатационные материалы.

## Безопасность

Не коммитьте реальные секреты и пользовательские данные:

- `.env`;
- токены и пароли;
- SMTP-ключи;
- локальные базы данных;
- `.venv`;
- пользовательские файлы из `media/`.

Для примеров используйте только `.env.example` с безопасными placeholder.
