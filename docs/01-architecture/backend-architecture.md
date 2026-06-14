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
# Backend Architecture

## Общий подход

Backend ЦОС «Пифагор» строится как **модульный монолит** на Django.

Это означает, что проект остаётся единым Django-приложением, но внутри разделён на независимые предметные модули. Такой подход проще поддерживать, тестировать и развивать на этапе личного продукта, чем ранний переход к микросервисам.

---

## Почему модульный монолит

Модульный монолит подходит проекту, потому что доменная модель сильно связана, пользователи, роли, курсы, задания, журнал и расписание должны работать в одной системе, проще вести транзакции, проще отлаживать, проще разворачивать и проще развивать одному или небольшой командой.

---

## Общая структура backend

```text
backend/
 ┣ apps/
 ┃ ┣ users/
 ┃ ┣ organizations/
 ┃ ┣ education/
 ┃ ┣ courses/
 ┃ ┣ lessons/
 ┃ ┣ assignments/
 ┃ ┣ testing/
 ┃ ┣ journal/
 ┃ ┣ schedule/
 ┃ ┣ materials/
 ┃ ┣ notifications/
 ┃ ┣ analytics/
 ┃ ┣ achievements/
 ┃ ┣ portfolio/
 ┃ ┣ projects/
 ┃ ┣ olympiads/
 ┃ ┣ ai/
 ┃ ┗ core/
 ┣ config/
 ┣ fixtures/
 ┣ media/
 ┣ static/
 ┣ tests/
 ┗ manage.py
```

---

## Типовая структура Django app

```text
app_name/
 ┣ models.py
 ┣ serializers.py
 ┣ views.py
 ┣ urls.py
 ┣ permissions.py
 ┣ services.py
 ┣ selectors.py
 ┣ validators.py
 ┣ tasks.py
 ┣ admin.py
 ┣ tests/
 ┗ migrations/
```

---

## Назначение файлов

`models.py` хранит модели данных и простую доменную логику, связанную с состоянием модели. `serializers.py` отвечает за преобразование данных между моделями и API. `views.py` содержит endpoints, но не должен содержать тяжёлую бизнес-логику. `permissions.py` описывает правила доступа. `services.py` содержит бизнес-операции. `selectors.py` содержит функции выборки данных. `validators.py` содержит доменные проверки. `tasks.py` содержит фоновые задачи.

---

## Основные backend-модули

- `users` — пользователи, роли, профили, настройки.
- `organizations` — образовательные организации, группы, членство, учебные периоды.
- `courses` — курсы, дисциплины, зачисления, преподаватели курса.
- `lessons` — уроки, структура урока, материалы, активности.
- `assignments` — задания, сдача работ, проверка, комментарии.
- `testing` — тесты, вопросы, попытки, результаты.
- `journal` — оценки, посещаемость, журнал, история изменений.
- `schedule` — расписание, кабинеты, временные слоты, замены.
- `materials` — файлы, учебные материалы, коллекции, версии.
- `notifications` — уведомления и настройки уведомлений.
- `analytics` — прогресс, рекомендации, сигналы риска.
- `ai` — ИИ-помощник «Анастасия», провайдеры, промпты, история запросов.
- `olympiads` — олимпиады, туры, задания, участники, проверки, апелляции.

---

## Правило бизнес-логики

View должен быть тонким. Бизнес-сценарии должны жить в `services.py`, а сложные выборки — в `selectors.py`.

```python
class AssignmentSubmitView(APIView):
    def post(self, request, assignment_id):
        result = submit_assignment(
            assignment_id=assignment_id,
            student=request.user,
            data=request.data,
        )
        return Response(AssignmentSubmissionSerializer(result).data)
```

---

## Авторизация и доступы

Backend должен поддерживать JWT access/refresh tokens, роли пользователя, членство в организации, объектные права, проверки доступа на уровне API и ограничения доступа по организации.

Один пользователь может иметь несколько ролей.

---

## Перспектива масштабирования

На старте все модули живут внутри монолита. В будущем можно вынести отдельно ИИ-Анастасию, олимпиады, аналитику, файловое хранилище, уведомления и видеозанятия.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
