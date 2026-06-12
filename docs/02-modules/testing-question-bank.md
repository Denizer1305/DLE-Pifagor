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
# Testing: банк вопросов

Банк вопросов хранит повторно используемые шаблоны заданий. Он нужен, чтобы преподаватель мог подготовить вопрос один раз, переиспользовать его в разных тестах и поддерживать общий набор заданий по организации и предмету.

## Основные сущности

| Модель | Назначение |
| --- | --- |
| `QuestionBankItem` | Шаблон вопроса: текст, тип, режим проверки, баллы, сложность, теги, владелец, организация, предмет, статус и видимость. |
| `QuestionBankOption` | Вариант ответа для шаблона вопроса. Используется для choice-вопросов. |
| `TestQuestion.source_bank_item` | Ссылка на шаблон, из которого был создан вопрос теста. |

## Поля `QuestionBankItem`

Ключевые поля:

- `title` - короткое название шаблона;
- `text` - текст вопроса;
- `explanation` - пояснение;
- `question_type` - тип вопроса;
- `check_mode` - автоматическая или ручная проверка;
- `expected_text_answer`, `expected_number_answer`, `case_sensitive` - ожидаемые ответы для text/number вопросов;
- `score` - базовый балл;
- `difficulty` - сложность;
- `tags_data` - теги;
- `organization`, `subject`, `owner_teacher` - область владения;
- `visibility` - приватный/организационный уровень видимости;
- `status` - черновик, опубликован, архив;
- `is_active` - мягкая активность.

## Поля `QuestionBankOption`

- `bank_item` - шаблон вопроса;
- `text` - текст варианта;
- `order` - порядок;
- `is_correct` - правильный вариант;
- `score` - балл за вариант;
- `feedback` - пояснение;
- `is_active` - мягкая активность.

## API

Банк доступен в admin и teacher зонах:

```text
GET/POST      /api/v1/testing/admin/bank-items/
GET/PATCH     /api/v1/testing/admin/bank-items/{id}/
GET/POST      /api/v1/testing/admin/bank-options/
GET/PATCH     /api/v1/testing/admin/bank-options/{id}/

GET/POST      /api/v1/testing/teacher/bank-items/
GET/PATCH     /api/v1/testing/teacher/bank-items/{id}/
GET/POST      /api/v1/testing/teacher/bank-options/
GET/PATCH     /api/v1/testing/teacher/bank-options/{id}/
```

Viewsets:

- `QuestionBankItemViewSet`;
- `QuestionBankOptionViewSet`.

## Жизненный цикл шаблона

1. Преподаватель создает `QuestionBankItem` в статусе черновика.
2. Для choice-вопросов добавляются `QuestionBankOption`.
3. Валидаторы проверяют тип вопроса, режим проверки, варианты и ожидаемые ответы.
4. Шаблон публикуется.
5. Опубликованный шаблон можно использовать как источник для `TestQuestion`.
6. При создании вопроса теста сохраняется ссылка `source_bank_item`.
7. Шаблон можно архивировать без удаления уже созданных вопросов тестов.

## Валидация

Валидация находится в:

```text
apps/testing/validators/bank/
apps/testing/validators/question/bank_source.py
```

Проверяются:

- соответствие типа вопроса и доступных полей ответа;
- корректность вариантов для choice-вопросов;
- наличие правильного ответа там, где он нужен;
- допустимость публикации;
- возможность использовать шаблон как источник вопроса.

## Сервисы и selectors

Основные файлы:

```text
apps/testing/services/bank/
apps/testing/selectors/bank/
apps/testing/managers/bank/
```

Правило: viewset не должен сам решать, можно ли публиковать или архивировать шаблон. Эти правила должны оставаться в validators/services.

## Админка

Django admin для банка находится в:

```text
apps/testing/admin/bank/
```

Админка поддерживает работу с `QuestionBankItem` и inline/options для вариантов ответа.

## Тесты

Покрытие банка:

```text
apps/testing/tests/api/test_admin_question_bank_api.py
apps/testing/tests/api/test_teacher_question_bank_api.py
apps/testing/tests/models/test_bank_models.py
apps/testing/tests/selectors/test_bank_selectors.py
apps/testing/tests/services/test_bank_services.py
apps/testing/tests/validators/test_bank_validators.py
```

При изменении банка нужно проверять API обеих ролей: admin и teacher.
