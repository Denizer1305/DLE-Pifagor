# Пифагор — backend

Backend образовательной платформы «Пифагор» на Django и Django REST Framework. Проект обслуживает авторизацию, пользователей, личные кабинеты, профиль, настройки, календарь, заметки, уведомления, обращения и образовательные сущности.

## Основные приложения

- `users` — пользователи, роли, профиль, настройки, административное управление аккаунтами.
- `dashboard` — backend-сводки для ЛК администратора, преподавателя, студента и родителя.
- `notifications` — уведомления, настройки доставки, прочтение и генерация событий.
- `feedback` — обращения пользователей, вложения, статусы и уведомления администратора.
- `organizations` — образовательные организации, структура, коды организаций.
- `education`, `courses`, `lessons`, `assignments`, `schedule` — образовательный контур платформы.
- `achievements`, `portfolio`, `projects`, `olympiads`, `testing`, `journal`, `materials`, `analytics`, `ai` — дополнительные доменные области.

## Структура

```text
apps/
  <module>/
    api|views/        HTTP endpoints and DRF viewsets
    serializers/     validation and API representation
    services/        business logic
    selectors/       read models and optimized queries
    models/          database models
    permissions/     access rules
    tests/           API and service tests
config/              Django settings and project configuration
fixtures/            seed data
media/               uploaded files in local development
static/              static assets
templates/           email and server-rendered templates
```

Новые крупные файлы нужно декомпозировать по папкам. Целевой ориентир для файлов serializer/view/test — до 200 строк, если функциональность уже распадается на самостоятельные части.

## Запуск

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements/dev.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

На Windows PowerShell путь к Python внутри окружения обычно выглядит так:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

## Проверки

```sh
DJANGO_SETTINGS_MODULE=config.settings.test .venv/bin/python manage.py check
DJANGO_SETTINGS_MODULE=config.settings.test .venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python -m ruff check apps config
.venv/bin/python -m black --check apps config
.venv/bin/python -m isort --profile black -o apps -o config --check-only apps config
```

Для форматирования:

```sh
.venv/bin/python -m black apps config
.venv/bin/python -m isort --profile black -o apps -o config apps config
```

## Реализованные API-направления

- Авторизация, refresh-сессии и редирект frontend при `401 Unauthorized`.
- Профиль пользователя, резервный email, телефон, город через endpoints DaData, avatar upload.
- Пользовательские настройки: внешний вид, язык, уведомления, приватность, роли, безопасность.
- Dashboard-сводки для ролей администратора, преподавателя, студента и родителя.
- Календарные события и заметки с отображением в ЛК и на страницах календаря/заметок.
- Уведомления с настройками, счётчиками, прочтением и интеграцией с событиями платформы.
- Обращения пользователей с вложениями, статусами, email-шаблоном и уведомлениями.
- Административный список пользователей, карточка пользователя, редактирование и жизненный цикл аккаунта.

## Контракты с frontend

Frontend ожидает REST API в формате DTO, которые затем преобразуются mapper-слоем. При изменении serializer-полей нужно обновлять:

- `src/modules/<module>/types/*.types.ts`;
- `src/modules/<module>/mappers/*.mapper.ts`;
- соответствующий service/composable;
- тесты backend API.

Для административного создания пользователя frontend отправляет `POST /api/v1/users/admin/users/`. Если endpoint не поддерживает создание, нужно добавить create serializer/service/viewset flow и вернуть `AdminUserDetailSerializer`.

## Правила разработки

- Views принимают HTTP-запрос и делегируют работу serializer/service.
- Serializers валидируют вход и описывают API-представление.
- Selectors отвечают за чтение и оптимизированные queryset.
- Services выполняют бизнес-операции и аудит.
- Permissions проверяют доступ по ролям.
- Тесты покрывают API-контракты, права доступа и важные service-сценарии.
