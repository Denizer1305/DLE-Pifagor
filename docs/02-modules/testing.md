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
# Testing

Модуль `testing` отвечает за учебные тесты: создание структуры теста, банк вопросов, прохождение обучающимся, сохранение ответов, автоматическую и ручную проверку, итоговые результаты и отчеты добросовестности.

## Зона ответственности

- хранение тестов, вопросов, вариантов ответов и результатов;
- управление попытками прохождения теста;
- проверка ответов в автоматическом и ручном режимах;
- публикация итогов для обучающегося и родителя;
- банк повторно используемых заданий;
- контроль рисков добросовестности попытки;
- API для администратора, преподавателя и обучающегося.

## Основные модели

| Модель | Назначение |
| --- | --- |
| `Test` | Учебный тест, привязанный к курсу, уроку/блоку, организации, предмету и преподавателю-владельцу. |
| `TestQuestion` | Вопрос конкретного теста. Может быть создан вручную или из `QuestionBankItem`. |
| `TestQuestionOption` | Вариант ответа для вопроса теста. |
| `TestAttempt` | Попытка обучающегося пройти тест. Хранит статус, проверку, баллы, дедлайн и видимость результата. |
| `TestAttemptAnswer` | Ответ обучающегося на вопрос в рамках попытки. |
| `TestLearnerResult` | Итоговая агрегированная запись результата обучающегося по тесту. |
| `QuestionBankItem` | Шаблон вопроса в банке заданий. |
| `QuestionBankOption` | Вариант ответа шаблона вопроса в банке. |
| `TestAttemptIntegrityReport` | Сохраненный отчет о рисках добросовестности попытки. |

## Ролевые API-зоны

Базовое подключение модуля разделено на три области:

```text
/api/v1/testing/admin/
/api/v1/testing/teacher/
/api/v1/testing/learner/
```

### Admin

Администратор работает со всеми основными сущностями:

```text
GET/POST      /api/v1/testing/admin/tests/
GET/PATCH     /api/v1/testing/admin/tests/{id}/
GET/POST      /api/v1/testing/admin/questions/
GET/POST      /api/v1/testing/admin/options/
GET/POST      /api/v1/testing/admin/attempts/
GET/POST      /api/v1/testing/admin/answers/
GET           /api/v1/testing/admin/results/
GET/POST      /api/v1/testing/admin/bank-items/
GET/POST      /api/v1/testing/admin/bank-options/
GET           /api/v1/testing/admin/integrity-reports/
GET           /api/v1/testing/admin/review/queue/
GET           /api/v1/testing/admin/review/teacher-summary/
GET           /api/v1/testing/admin/review/test-summary/
POST          /api/v1/testing/admin/review/recalculate-attempt/
```

### Teacher

Преподаватель использует те же viewsets, но доступ ограничивается правами и scope преподавателя:

```text
/api/v1/testing/teacher/tests/
/api/v1/testing/teacher/questions/
/api/v1/testing/teacher/options/
/api/v1/testing/teacher/attempts/
/api/v1/testing/teacher/answers/
/api/v1/testing/teacher/results/
/api/v1/testing/teacher/bank-items/
/api/v1/testing/teacher/bank-options/
/api/v1/testing/teacher/integrity-reports/
/api/v1/testing/teacher/review/
```

### Learner

Обучающийся видит доступные тесты, свои попытки и результаты, а прохождение идет через отдельный `taking` API:

```text
GET           /api/v1/testing/learner/tests/
GET           /api/v1/testing/learner/attempts/
GET           /api/v1/testing/learner/results/
POST          /api/v1/testing/learner/taking/start/
GET           /api/v1/testing/learner/taking/active/?test_id={id}
POST          /api/v1/testing/learner/taking/save-answers/
POST          /api/v1/testing/learner/taking/submit/
```

## Жизненный цикл теста

1. Преподаватель или администратор создает `Test` в статусе черновика.
2. В тест добавляются `TestQuestion` и `TestQuestionOption`.
3. Вопросы могут быть созданы вручную или на основе `QuestionBankItem`.
4. Тест публикуется и становится доступным обучающимся по правилам видимости.
5. Обучающийся начинает `TestAttempt`.
6. Ответы сохраняются через taking flow.
7. Попытка отправляется на проверку.
8. Автопроверка считает баллы для вопросов с автоматическим режимом.
9. Если есть ручные вопросы, попытка попадает в очередь проверки.
10. После подтверждения результата обновляется `TestLearnerResult`.
11. Для попытки формируется `TestAttemptIntegrityReport`.

## Проверка ответов

Автоматическая проверка поддерживает:

- single choice;
- true/false;
- multiple choice;
- number;
- short text при наличии ожидаемого ответа.

Ручная проверка нужна, если:

- у вопроса `check_mode = manual`;
- тип вопроса не может быть надежно проверен автоматически;
- short text не имеет ожидаемого ответа;
- преподаватель должен выставить балл и комментарий.

## Сервисный слой

Основные зоны services:

```text
services/test/
services/question/
services/bank/
services/attempt/
services/checking/
services/result/
services/review/
services/taking/
services/integrity/
```

Правило развития: views принимают HTTP-запрос и делегируют в serializer/selector/service. Новая бизнес-логика не должна жить во viewset.

## Связанные документы

- [Банк вопросов](./testing-question-bank.md)
- [Прохождение теста обучающимся](./testing-learner-flow.md)
- [Контроль добросовестности](./testing-integrity.md)

## Тестовое покрытие

Ключевые группы тестов:

```text
apps/testing/tests/api/
apps/testing/tests/models/
apps/testing/tests/selectors/
apps/testing/tests/services/
apps/testing/tests/validators/
```

При изменении модели или API нужно обновлять:

- serializer contract;
- permissions;
- selectors;
- service tests;
- API tests соответствующей ролевой зоны.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
