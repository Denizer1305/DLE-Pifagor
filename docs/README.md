<!-- DLE-Pifagor README Header -->
<p align="center">
  <a href="../README.md"><img src="../design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Документация проекта и материалы разработки</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor README Header -->
# Документация DLE-Pifagor

Эта папка хранит продуктовую, архитектурную, пользовательскую и инженерную
документацию образовательной платформы **ЦОС "Пифагор"**.

Документация нужна как рабочая карта проекта: где лежат модули, как устроены
backend и frontend, какие API-контракты доступны, как запускать проверки и где
фиксировать архитектурные решения.

## Структура

```text
docs/
  00-vision/          продуктовая идея, миссия, позиционирование и roadmap
  01-architecture/    архитектура backend, frontend, API, данных и репозитория
  02-modules/         описание функциональных модулей платформы
  03-design-system/   UI-принципы, цвета, типографика, компоненты и темы
  04-development/     локальный запуск, правила разработки, CI, git и deploy
  05-user-guides/     пользовательские инструкции по ролям
  06-api/             OpenAPI, API-правила и snapshot схемы
  07-operations/      release checklist и troubleshooting
  decisions/          ADR: принятые архитектурные решения
```

## Быстрые входные точки

| Раздел | Файл |
| --- | --- |
| Видение продукта | `00-vision/product-vision.md` |
| Структура проекта | `01-architecture/project-structure.md` |
| Backend-архитектура | `01-architecture/backend-architecture.md` |
| Frontend-архитектура | `01-architecture/frontend-architecture.md` |
| API-архитектура | `01-architecture/api-architecture.md` |
| OpenAPI | `06-api/openapi.md` |
| Локальный запуск | `04-development/local-setup.md` |
| Правила разработки | `04-development/coding-rules.md` |
| Стратегия тестирования | `04-development/testing-strategy.md` |
| Release checklist | `07-operations/release-checklist.md` |

## Модули платформы

Основные продуктовые модули описаны в `02-modules/`:

- `users.md` - пользователи, роли, профили и настройки аккаунта;
- `organizations.md` - организации, отделения, группы, предметы и связи;
- `courses.md` - курсы, уроки, материалы и прогресс;
- `testing.md` - тесты, попытки, результаты и роли участников;
- `testing-question-bank.md` - банк вопросов и варианты ответов;
- `testing-learner-flow.md` - прохождение тестов учеником;
- `testing-integrity.md` - контроль целостности попыток и отчеты;
- `calendar-and-notes.md` - календарь, план на день и заметки;
- `notifications.md` - уведомления, счетчики и пользовательские настройки;
- `feedback.md` - публичные обращения и административная обработка;
- `settings.md` - внешний вид, язык, приватность, безопасность и роли;
- `assignments.md`, `journal.md`, `schedule.md`, `olympiads.md`,
  `ai-anastasia.md` - расширяемые учебные и сервисные направления.

## API и OpenAPI

Backend публикует документацию API через `drf-spectacular`:

- `/api/schema/` - машинно-читаемая OpenAPI-схема;
- `/api/docs/` - Swagger UI;
- `/api/redoc/` - ReDoc.

Snapshot схемы хранится в `06-api/openapi.yaml`. Правила обновления описаны в
`06-api/openapi.md`.

## Разработка

Для локального запуска и проверок используйте корневой `Makefile`:

```sh
make backend-run
make frontend-run
make backend-ci
make frontend-ci
make check
```

Точечные команды для Windows PowerShell, backend и frontend приведены в
`04-development/local-setup.md`.

## Поддержание порядка

При изменении функциональности обновляйте:

- соответствующий файл в `02-modules/`;
- `06-api/openapi.yaml`, если изменились маршруты, serializers или responses;
- архитектурные документы из `01-architecture/`, если изменились слои,
  зависимости или структура модулей;
- ADR в `decisions/`, если принято заметное архитектурное решение;
- пользовательские инструкции в `05-user-guides/`, если изменился сценарий роли.

---
<!-- DLE-Pifagor README Footer -->
<p align="center">
  <sub>ЦОС "Пифагор" · единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>
<!-- /DLE-Pifagor README Footer -->
