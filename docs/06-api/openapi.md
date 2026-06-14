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
# OpenAPI

OpenAPI-документация проекта формируется backend-частью через `drf-spectacular`.
Конфигурация подключена в `config/settings/base.py`, а публичные маршруты схемы
описаны в `config/urls.py`.

## Где смотреть схему

Актуальные endpoint backend:

- `/api/schema/` - машинно-читаемая OpenAPI-схема;
- `/api/docs/` - Swagger UI;
- `/api/redoc/` - ReDoc.

Сгенерированный snapshot схемы хранится в репозитории:

- `docs/06-api/openapi.yaml`

## Как обновить snapshot

Команда запускается из папки `backend`.

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.test"
..\.venv\Scripts\python.exe manage.py spectacular --file ..\docs\06-api\openapi.yaml
```

Если используется другой виртуальный environment, замените путь к `python.exe` на
актуальный для локального окружения.

## Что входит в схему

Схема собирает маршруты API проекта, включая основные домены:

- `users` - аутентификация, профиль, настройки пользователя;
- `organizations` - организации, участники, учебные группы и административные
  операции;
- `education` - предметы, периоды обучения, учебные сущности;
- `courses` и `materials` - курсы, уроки, материалы и прогресс;
- `testing` - банки вопросов, тесты, попытки, проверка и пересчет результатов;
- `dashboard` - сводки, виджеты и элементы панели;
- `notifications` - уведомления пользователя;
- `feedback` - обратная связь и публичные обращения.

## Текущее состояние схемы

Snapshot `openapi.yaml` сгенерирован успешно, но генератор пока сообщает о
неполной разметке части endpoint. Это не блокирует выгрузку файла, однако влияет
на полноту контракта для клиентов и автогенерации SDK.

Основные замечания генератора:

- часть `APIView`/`ViewSet` не имеет явного `serializer_class` или
  `@extend_schema`, поэтому `drf-spectacular` не может надежно вывести запросы и
  ответы;
- есть конфликты имен компонентов для коротких serializers вроде `UserShort`,
  `OrganizationShort`, `SubjectShort`, `AcademicYearShort`,
  `EducationPeriodShort`;
- есть конфликты `operationId` у отдельных маршрутов `notifications` и
  административных маршрутов `organizations`;
- отдельные вычисляемые поля serializers требуют явного типа через type hint или
  `@extend_schema_field`;
- для повторяющихся enum-значений стоит добавить `ENUM_NAME_OVERRIDES` в
  `SPECTACULAR_SETTINGS`.

## Правила поддержки

После изменения serializers, views, permissions или маршрутов нужно обновлять
`docs/06-api/openapi.yaml` и проверять вывод `manage.py spectacular`.

Перед релизом желательно довести генерацию схемы до состояния без новых warnings:
добавлять `serializer_class`, `get_serializer_class`, `@extend_schema`,
`@extend_schema_view`, `OpenApiParameter`, `OpenApiResponse` и уникальные
`ref_name` там, где автоматического вывода недостаточно.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
