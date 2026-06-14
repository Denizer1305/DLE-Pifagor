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
# API Architecture

API ЦОС "Пифагор" строится как REST API на Django REST Framework. Frontend на
Vue работает с backend только через HTTP-контракты, а OpenAPI-схема выступает
общей точкой синхронизации backend и frontend.

## Версионирование

Основной префикс прикладных маршрутов:

```text
/api/v1/
```

Служебная документация схемы доступна отдельно:

```text
/api/schema/
/api/docs/
/api/redoc/
```

## Основные домены API

Фактические маршруты сгруппированы вокруг доменных модулей:

- `/api/v1/users/...` - auth, пользователи, роли, профили, настройки;
- `/api/v1/organizations/...` - организации, группы, предметы, кураторы,
  публичные данные организаций и преподавателей;
- `/api/v1/courses/...` - курсы, доступ, уроки и прогресс;
- `/api/v1/materials/...` - учебные материалы;
- `/api/v1/testing/...` - тесты, банк вопросов, попытки, результаты, review и
  integrity reports;
- `/api/v1/dashboard/...` - сводки личных кабинетов и элементы dashboard;
- `/api/v1/notifications/...` - уведомления, счетчики, прочтение и настройки;
- `/api/v1/feedback/...` - публичные обращения и административная обработка.

Точные маршруты фиксируются в `docs/06-api/openapi.yaml`.

## Разделение ответственности

Backend:

- `views` принимают HTTP-запрос, применяют permissions и вызывают serializer или
  service;
- `serializers` валидируют вход и описывают API-представление;
- `services` выполняют бизнес-операции и изменения состояния;
- `selectors` отвечают за чтение и оптимизированные queryset;
- `permissions` фиксируют правила доступа по ролям и объектным связям.

Frontend:

- `api` выполняет HTTP-запросы;
- `services` собирают сценарии работы с backend;
- `mappers` преобразуют DTO в UI-модели;
- `types` синхронизируются с backend serializers и OpenAPI.

## Авторизация

API использует JWT access/refresh token. Защищенные запросы передают access
token в заголовке:

```text
Authorization: Bearer <token>
```

Клиент должен обрабатывать:

- `401` - токен отсутствует, истек или refresh невозможен;
- `403` - пользователь авторизован, но не имеет прав на действие;
- `404` - объект недоступен или отсутствует;
- `409` - действие конфликтует с текущим состоянием объекта.

## OpenAPI

Схема формируется через `drf-spectacular`.

Актуальные endpoint:

- `/api/schema/` - машинно-читаемая схема;
- `/api/docs/` - Swagger UI;
- `/api/redoc/` - ReDoc.

Snapshot схемы хранится в `docs/06-api/openapi.yaml`. Обновлять его нужно после
изменения routes, serializers, permissions или формата ответов.

## Правила проектирования

- API должен отражать пользовательские сценарии, а не только структуру таблиц.
- Изменения serializer-полей считаются изменением контракта и требуют обновления
  frontend DTO/types.
- Нестандартные actions должны иметь явные request/response serializers.
- Для OpenAPI нужно добавлять `@extend_schema`, `@extend_schema_view`,
  `OpenApiParameter`, `OpenApiResponse` и уникальные `ref_name`, когда
  автоматического вывода недостаточно.
- Публичные endpoint не должны раскрывать внутренние административные поля.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
