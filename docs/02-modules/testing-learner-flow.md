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
# Testing: прохождение теста обучающимся

Learner flow описывает безопасное прохождение теста обучающимся: старт попытки, получение payload, сохранение ответов, отправка на проверку и получение результата.

## Основной API

Прохождение вынесено в отдельный viewset:

```text
/api/v1/testing/learner/taking/
```

Доступные actions:

```text
POST /api/v1/testing/learner/taking/start/
GET  /api/v1/testing/learner/taking/active/?test_id={id}
POST /api/v1/testing/learner/taking/save-answers/
POST /api/v1/testing/learner/taking/submit/
```

Дополнительно обучающийся может читать:

```text
GET /api/v1/testing/learner/tests/
GET /api/v1/testing/learner/attempts/
GET /api/v1/testing/learner/results/
```

## Start

`POST /taking/start/`

Назначение:

- проверить, что тест доступен обучающемуся;
- вернуть активную попытку, если она уже есть;
- создать новую попытку, если активной попытки нет;
- вернуть payload теста для прохождения.

Минимальное тело:

```json
{
  "test_id": 1
}
```

Сервисный путь:

```text
TestTakingViewSet.start
ensure_learner_can_take_test
get_active_attempt_for_taking
start_test_attempt
build_taking_test_payload
```

## Active

`GET /taking/active/?test_id={id}`

Назначение:

- вернуть текущую активную попытку;
- восстановить экран прохождения после перезагрузки страницы;
- не создавать новую попытку.

Если активной попытки нет, API возвращает `404`.

## Save answers

`POST /taking/save-answers/`

Назначение:

- сохранить один или несколько ответов в рамках активной попытки;
- обновить уже существующий ответ на тот же вопрос;
- не отправлять попытку на проверку.

Типовой payload:

```json
{
  "attempt_id": 10,
  "answers": [
    {
      "question_id": 100,
      "selected_option_id": 500
    },
    {
      "question_id": 101,
      "text_answer": "Ответ"
    }
  ]
}
```

Сервисный путь:

```text
TestTakingViewSet.save_answers
get_taking_attempt_by_id
ensure_learner_can_continue_attempt
save_attempt_answers
save_attempt_answer
validate_answer
```

Ограничения:

- ответы можно сохранять только для попытки в статусе `started`;
- попытка должна принадлежать текущему пользователю;
- если у теста есть лимит времени, попытка не должна быть просрочена.

## Submit

`POST /taking/submit/`

Назначение:

- завершить попытку;
- перевести ее на проверку;
- запустить автопроверку;
- сформировать отчет добросовестности;
- вернуть обновленную попытку.

Минимальное тело:

```json
{
  "attempt_id": 10
}
```

Сервисный путь:

```text
TestTakingViewSet.submit
get_taking_attempt_by_id
ensure_learner_can_continue_attempt
submit_test_attempt
auto_check_attempt_task
build_and_save_attempt_integrity_report_task
```

## Статусы попытки

Ключевые состояния `TestAttempt`:

- `started` - обучающийся проходит тест;
- `submitted` - попытка отправлена;
- `auto_checked` - автопроверка завершена;
- `needs_review` - требуется ручная проверка;
- `confirmed` - преподаватель подтвердил результат;
- `cancelled` - попытка отменена;
- `expired` - время попытки истекло.

Точные значения берутся из `apps/testing/constants/attempt/choices.py`.

## Лимит времени

Если у теста задан `time_limit_minutes`, при старте попытки рассчитывается `expires_at`.

Проверки времени находятся в:

```text
apps/testing/services/attempt/time_limit.py
apps/testing/validators/attempt/time_limit.py
```

Важные правила:

- после истечения времени нельзя сохранять ответы;
- после истечения времени нельзя штатно отправить попытку без обработки expiration flow;
- просрочка фиксируется через `expire_attempt_if_needed` и `expire_attempt_task`.

## Автопроверка

Автопроверка запускается после submit:

```text
apps/testing/tasks/attempt/tasks.py
apps/testing/services/checking/auto_check.py
```

Автоматически проверяются:

- single choice;
- true/false;
- multiple choice;
- number;
- short text при наличии ожидаемого ответа.

Если вопрос требует ручной проверки, ответ и попытка помечаются как `requires_manual_review`.

## Результат

После проверки и подтверждения результата обновляется `TestLearnerResult`.

Итоговая запись хранит:

- количество попыток;
- количество подтвержденных попыток;
- средний балл;
- лучший балл;
- итоговую оценку;
- флаги видимости для обучающегося и родителя.

## Frontend contract

Frontend должен:

- стартовать прохождение через `/taking/start/`;
- периодически сохранять ответы через `/taking/save-answers/`;
- восстанавливать попытку через `/taking/active/`;
- отправлять попытку только один раз через `/taking/submit/`;
- учитывать `expires_at` из payload попытки;
- не показывать правильные ответы до публикации/разрешения backend.
