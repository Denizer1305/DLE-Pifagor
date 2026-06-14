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
# API

Раздел описывает правила работы с API ЦОС "Пифагор": авторизацию, роли,
ошибки, OpenAPI-документацию и взаимодействие frontend-клиентов с backend.

## Авторизация

API использует JWT access/refresh token. Клиент должен:

- прикладывать access token к защищенным запросам;
- обновлять access token через refresh endpoint;
- перенаправлять пользователя на страницу входа, если refresh невозможен;
- не отправлять защищенные запросы без токена.

Токен передается в заголовке:

```text
Authorization: Bearer <access_token>
```

## Роли и доступ

Доступ к личным кабинетам и административным endpoint зависит от роли
пользователя, активной роли и объектных связей: организации, группы,
преподавателя, ученика или родителя.

- `401` - нет действительных учетных данных;
- `403` - пользователь авторизован, но не имеет прав на действие;
- `404` - объект не найден или скрыт политикой доступа;
- `409` - конфликт состояния, если действие невозможно в текущем статусе.

## OpenAPI

Backend публикует схему через `drf-spectacular`:

- `/api/schema/` - OpenAPI schema;
- `/api/docs/` - Swagger UI;
- `/api/redoc/` - ReDoc.

Snapshot схемы хранится в `docs/06-api/openapi.yaml`. Инструкция обновления и
текущие ограничения описаны в `docs/06-api/openapi.md`.

## Frontend API-клиенты

Frontend хранит API-слой внутри модулей:

- `api` - низкоуровневые HTTP-запросы;
- `services` - сценарии работы с backend;
- `mappers` - преобразование DTO в UI-модели;
- `types` - типы DTO, payload и доменных моделей.

При изменении backend serializer или response нужно синхронно обновлять
frontend-типы, mapper и сервис соответствующего модуля.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
