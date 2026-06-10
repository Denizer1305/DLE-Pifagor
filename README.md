<!-- DLE-Pifagor Root Header -->
<p align="center">
  <a href="README.md"><img src="design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Корневая документация проекта · README проекта</sub>
</p>

<p align="center">
  <a href="README.md">README проекта</a> ·
  <a href="docs/README.md">Документация</a> ·
  <a href="README.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor Root Header -->

## О проекте

**ЦОС "Пифагор"** - дипломная образовательная платформа, которая объединяет публичный сайт, авторизацию, личные кабинеты администратора, преподавателя, студента и родителя, управление пользователями, образовательными организациями, календарем, заметками, уведомлениями, обращениями и настройками.

Проект строится как единая цифровая образовательная среда: backend отвечает за доменную модель, API, права доступа, уведомления и обработку данных, а frontend предоставляет ролевые рабочие пространства с единой дизайн-системой.

## Быстрые ссылки

| Раздел | Ссылка |
| --- | --- |
| Общая документация | [`docs/README.md`](docs/README.md) |
| Backend | [`backend/README.md`](backend/README.md) |
| Frontend | [`frontend/README.md`](frontend/README.md) |
| Дизайн и логотипы | [`design/README.md`](design/README.md) |
| Инфраструктура | [`infra/README.md`](infra/README.md) |
| Скрипты | [`scripts/README.md`](scripts/README.md) |
| GitHub Actions | [`.github/README.md`](.github/README.md) |
| API архитектура | [`docs/01-architecture/api-architecture.md`](docs/01-architecture/api-architecture.md) |
| Модули платформы | [`docs/02-modules/`](docs/02-modules/) |
| Правила разработки | [`docs/04-development/coding-rules.md`](docs/04-development/coding-rules.md) |
| Регламенты проекта | [`docs/governance/`](docs/governance/) |

## Стек

### Backend

- Python 3.12+
- Django 5
- Django REST Framework
- PostgreSQL
- Redis и Celery для фоновых задач
- django-filter
- drf-spectacular
- Ruff, Black, isort
- Django tests, coverage, GitHub Actions

### Frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- Font Awesome
- CSS modules by feature/domain

### Инфраструктура и качество

- GitHub Actions
- Прямые backend-проверки через Django, Ruff, Black и isort
- Отдельные CI workflow для backend и frontend
- Документация по модулям, архитектуре и решениям

## Реализованные области

- Публичные страницы: главная, о платформе, преподаватели, контакты.
- Авторизация: вход, регистрация, подтверждение email, восстановление пароля, выход.
- Личные кабинеты: администратор, преподаватель, студент, родитель.
- Профиль пользователя: просмотр, редактирование, аватар, контакты, город, приватность.
- Настройки: внешний вид, темы, язык, уведомления, приватность, роли, безопасность.
- Администрирование пользователей: список, фильтры, создание, карточка, редактирование.
- Организации: организации, отделения, группы, предметы, преподаватели, кураторы, заявки, коды.
- Календарь и заметки: события, план на день, заметки на календаре, отдельная страница заметок.
- Уведомления: счетчики, dropdown, страница уведомлений, настройки уведомлений.
- Обращения: форма пользователя, вложения, уведомления, административная обработка.
- Страницы ошибок и технические заглушки в едином стиле платформы.

## Структура репозитория

```text
DLE-Pifagor/
├─ .github/          # GitHub Actions и настройки репозитория
├─ backend/          # Django backend и API
├─ design/           # бренд, логотипы, презентации и визуальные материалы
├─ docs/             # архитектура, модули, дизайн-система, ADR
├─ frontend/         # Vue frontend
├─ infra/            # Docker, nginx, deploy и эксплуатационные заметки
├─ scripts/          # проектные утилиты
├─ README.md         # русская версия
└─ README.en.md      # английская версия
```

## Быстрый старт

### Backend

```bash
cd backend
python manage.py check --settings=config.settings.test
python manage.py makemigrations --check --dry-run --settings=config.settings.test
python -m ruff check apps config
python -m black --check apps config
python -m isort --profile black -o apps -o config --check-only apps config
python manage.py test --settings=config.settings.test
```
### Frontend

```bash
cd frontend
npm run typecheck
npm run build
```

## Документация

Начните с [`docs/README.md`](docs/README.md). Там собраны ссылки на продуктовые документы, архитектуру, описание модулей, дизайн-систему, правила разработки и ADR.

Полезные точки входа:

- [`docs/00-vision/product-vision.md`](docs/00-vision/product-vision.md)
- [`docs/01-architecture/project-structure.md`](docs/01-architecture/project-structure.md)
- [`docs/01-architecture/backend-architecture.md`](docs/01-architecture/backend-architecture.md)
- [`docs/01-architecture/frontend-architecture.md`](docs/01-architecture/frontend-architecture.md)
- [`docs/02-modules/users.md`](docs/02-modules/users.md)
- [`docs/02-modules/organizations.md`](docs/02-modules/organizations.md)
- [`docs/02-modules/calendar-and-notes.md`](docs/02-modules/calendar-and-notes.md)
- [`docs/02-modules/notifications.md`](docs/02-modules/notifications.md)
- [`docs/02-modules/feedback.md`](docs/02-modules/feedback.md)
- [`docs/02-modules/settings.md`](docs/02-modules/settings.md)

## Работа с ветками и коммитами

Соглашение по коммитам описано в [`docs/04-development/commit-convention.md`](docs/04-development/commit-convention.md).

Примеры:

```bash
git commit -m "feat(frontend): Добавлена страница управления организациями"
git commit -m "fix(backend): Исправлена выдача уведомлений"
git commit -m "docs(project): Обновлена корневая документация"
```

## Безопасность

Не коммитьте реальные секреты и пользовательские данные:

- `.env`;
- токены;
- пароли;
- SMTP-ключи;
- локальные базы данных;
- `.venv`;
- пользовательские файлы из `media/`.

Для примеров используйте только `.env.example` с безопасными placeholder-значениями.

## Статус

Проект находится в активной разработке. Документация и README должны обновляться вместе с функциональными модулями, API, настройками CI и изменениями архитектуры.
---

<!-- DLE-Pifagor Root Footer -->
---

<p align="center">
  <sub>ЦОС "Пифагор" · единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="README.md">README проекта</a> ·
  <a href="docs/README.md">Документация</a> ·
  <a href="README.en.md">English version</a>
</p>
<!-- /DLE-Pifagor Root Footer -->
