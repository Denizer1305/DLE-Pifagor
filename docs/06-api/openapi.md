# OpenAPI

## Где смотреть схему

OpenAPI-схема формируется backend через drf-spectacular, если это включено настройками окружения.

Типовой набор endpoint:

- `/api/schema/` - JSON/YAML schema;
- `/api/schema/swagger-ui/` - Swagger UI;
- `/api/schema/redoc/` - ReDoc.

## Правила обновления

После изменения serializers, views, permissions или маршрутов проверьте, что схема отражает новое поведение.

## Что документировать вручную

OpenAPI не заменяет продуктовую документацию. В `docs/02-modules` нужно описывать сценарии пользователя, ограничения и связи модулей.
