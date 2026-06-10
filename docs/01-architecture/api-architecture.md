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

## Общий подход

API ЦОС «Пифагор» строится как REST API на базе Django REST Framework.

Frontend на Vue общается с backend только через API. Это позволяет разделить пользовательский интерфейс и бизнес-логику, а в будущем подключить мобильное приложение или внешние интеграции.

---

## Версионирование API

Все endpoints должны иметь версию.

```text
/api/v1/
```

---

## Принципы проектирования API

API должен быть предсказуемым, единообразным, документированным, защищённым, ролевым, пагинированным и удобным для frontend.

---

## Основные endpoints

### Auth

```text
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
GET  /api/v1/auth/me/
```

### Users

```text
GET    /api/v1/users/me/
PATCH  /api/v1/users/me/
GET    /api/v1/users/
GET    /api/v1/users/{id}/
```

### Organizations

```text
GET    /api/v1/organizations/
POST   /api/v1/organizations/
GET    /api/v1/organizations/{id}/
PATCH  /api/v1/organizations/{id}/
GET    /api/v1/organizations/{id}/groups/
```

### Courses

```text
GET    /api/v1/courses/
POST   /api/v1/courses/
GET    /api/v1/courses/{id}/
PATCH  /api/v1/courses/{id}/
DELETE /api/v1/courses/{id}/
GET    /api/v1/courses/{id}/lessons/
```

### Lessons

```text
GET    /api/v1/lessons/
POST   /api/v1/lessons/
GET    /api/v1/lessons/{id}/
PATCH  /api/v1/lessons/{id}/
DELETE /api/v1/lessons/{id}/
GET    /api/v1/lessons/{id}/materials/
GET    /api/v1/lessons/{id}/assignments/
```

### Assignments

```text
GET    /api/v1/assignments/
POST   /api/v1/assignments/
GET    /api/v1/assignments/{id}/
PATCH  /api/v1/assignments/{id}/
POST   /api/v1/assignments/{id}/submit/
GET    /api/v1/assignments/{id}/submissions/
POST   /api/v1/submissions/{id}/review/
```

### Journal

```text
GET    /api/v1/journal/
GET    /api/v1/journal/groups/{group_id}/
POST   /api/v1/grades/
PATCH  /api/v1/grades/{id}/
GET    /api/v1/students/{id}/grades/
```

### Schedule

```text
GET    /api/v1/schedule/
POST   /api/v1/schedule/
GET    /api/v1/schedule/{id}/
PATCH  /api/v1/schedule/{id}/
DELETE /api/v1/schedule/{id}/
POST   /api/v1/schedule/check-conflicts/
```

### AI Anastasia

```text
POST /api/v1/ai/chat/
POST /api/v1/ai/generate-lesson-plan/
POST /api/v1/ai/generate-assignment/
POST /api/v1/ai/explain-topic/
GET  /api/v1/ai/conversations/
```

---

## Формат ответа

Успешный ответ:

```json
{
    "data": {},
    "meta": {}
}
```

Ошибка:

```json
{
    "error": {
        "code": "permission_denied",
        "message": "У вас нет доступа к этому ресурсу.",
        "details": {}
    }
}
```

---

## Авторизация

Основной вариант: access token, refresh token, ролевые права и объектные права.

Frontend отправляет access token в заголовке:

```text
Authorization: Bearer <token>
```

---

## Ролевой доступ

API должен учитывать роль пользователя, организацию, группу, связь родителя с ребёнком, назначение преподавателя и права администратора.

---

## Документация API

API должен описываться через OpenAPI. Рекомендуемый инструмент — `drf-spectacular`.

```text
/api/schema/
/api/docs/
/api/redoc/
```

---

## Главный принцип API

API должен отражать реальные сценарии пользователей, а не только структуру таблиц базы данных.
---
---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
