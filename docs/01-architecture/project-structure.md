<!-- DLE-Pifagor Documentation Header -->
<p align="center">
  <a href="../../README.md"><img src="../../design/logos/main/pifagor-logo-primary.svg" alt="DLE-Pifagor" width="96" /></a>
</p>

<p align="center">
  <a href="../../docs/README.md">Документация</a> ·
  <a href="../../docs/README.en.md">English version</a> ·
  <a href="../../README.md">README проекта</a>
</p>

---
<!-- /DLE-Pifagor Documentation Header -->
# Project Structure

Документ фиксирует фактическую структуру монорепозитория ЦОС "Пифагор" и
правила размещения новых файлов.

## Корень репозитория

```text
DLE-Pifagor/
  .github/              GitHub Actions и настройки репозитория
  backend/              Django backend и REST API
  frontend/             Vue 3 frontend
  docs/                 проектная документация
  design/               бренд, логотипы и визуальные материалы
  infra/                Docker, nginx и эксплуатационные заметки
  scripts/              проектные утилиты
  docker-compose.yml    локальный запуск инфраструктуры
  Makefile              единые команды установки, запуска и проверок
  README.md             русская входная точка проекта
  README.en.md          английская входная точка проекта
```

## Backend

Backend находится в `backend/` и построен как Django modular monolith.

```text
backend/
  apps/
    core/               общие базовые сущности и инфраструктурные helpers
    users/              пользователи, роли, профили, настройки, auth
    organizations/      организации, группы, предметы и связи пользователей
    education/          учебные справочники и периоды
    course/             курсы, уроки, доступ и прогресс
    materials/          учебные материалы
    testing/            тесты, банк вопросов, попытки, проверка
    dashboard/          сводки и элементы личных кабинетов
    notifications/      уведомления и пользовательские настройки
    feedback/           обращения и административная обработка
    backoffice/         служебные административные сценарии
    ...                 расширяемые домены: schedule, journal, ai и другие
  config/               settings, urls, ASGI/WSGI
  requirements/         зависимости по окружениям
  manage.py
```

Внутри backend-модулей предпочтительна слоистая структура:

```text
models/                 модели данных
serializers/            DTO, validation, API representation
views/                  DRF views/viewsets
selectors/              optimized read queries
services/               business operations
permissions/            access rules
validators/             domain validation
tasks/                  background jobs
tests/                  API, selector и service tests
```

## Frontend

Frontend находится в `frontend/` и построен на Vue 3, TypeScript и Vite.

```text
frontend/
  src/
    app/                bootstrap, constants, global setup
    api/                общая HTTP-инфраструктура
    assets/             локальные assets
    components/         общие UI и dashboard-компоненты
    composables/        переиспользуемая Composition API логика
    i18n/               словари и сообщения интерфейса
    modules/            доменные frontend-модули
    pages/              общие страницы и error views
    router/             маршруты
    stores/             Pinia stores
    styles/             CSS по слоям и модулям
```

Доменные модули во frontend используют единую схему:

```text
api/                    низкоуровневые HTTP-запросы
services/               сценарии работы с backend
mappers/                преобразование DTO в UI-модели
types/                  DTO, payload и UI-типы
data/                   статичная конфигурация и тексты
composables/            состояние и пользовательские сценарии
components/             компоненты без маршрутизации
pages/                  тонкие страницы-сборщики
```

## Документация

`docs/` делится по назначению:

```text
00-vision/              продуктовая рамка
01-architecture/        архитектура и структура проекта
02-modules/             функциональные модули
03-design-system/       UI и визуальные правила
04-development/         разработка, запуск, CI, git
05-user-guides/         инструкции пользователей
06-api/                 API и OpenAPI
07-operations/          релизы и эксплуатация
decisions/              ADR
```

## Правила размещения

- Новый backend-код размещается в доменном приложении внутри `backend/apps`.
- Бизнес-логику не нужно держать во views: она уходит в `services`, чтение - в
  `selectors`.
- Новый frontend-код размещается в `src/modules/<domain>`, если он относится к
  предметной области.
- Страницы frontend должны оставаться тонкими: сборка layout, вызов composable,
  передача данных в компоненты.
- Общие UI-компоненты размещаются в `src/components`, если они реально
  переиспользуются несколькими модулями.
- Изменения API должны сопровождаться обновлением `docs/06-api/openapi.yaml` и
  соответствующих frontend `types/mappers/services`.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
