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
# Testing: контроль добросовестности

Контроль добросовестности фиксирует признаки риска при прохождении теста. Он не является доказательством списывания и используется как вспомогательный сигнал для преподавателя.

## Основная модель

`TestAttemptIntegrityReport` хранит один отчет на одну попытку:

| Поле | Назначение |
| --- | --- |
| `attempt` | Связанная попытка `TestAttempt`, связь one-to-one. |
| `score` | Итоговый риск в баллах. |
| `risk_level` | Уровень риска. |
| `flags_data` | Список признаков риска в JSON. |
| `checked_at` | Время анализа. |
| `created_at`, `updated_at` | Технические timestamps. |

Индексы заведены по `attempt`, `risk_level`, `score`, `checked_at`.

## Уровни риска

Точные значения определены в:

```text
apps/testing/constants/integrity/choices.py
```

Документационная семантика:

- low - низкий риск;
- medium - есть признаки, которые стоит просмотреть;
- high - высокий риск, нужна ручная проверка контекста.

## Когда формируется отчет

Отчет создается после отправки попытки:

```text
TestTakingViewSet.submit
build_and_save_attempt_integrity_report_task
build_and_save_attempt_integrity_report
save_attempt_integrity_report
```

Файлы:

```text
apps/testing/tasks/integrity/tasks.py
apps/testing/services/integrity/recalculation.py
apps/testing/services/integrity/persistence.py
```

## API

Отчеты доступны в admin и teacher зонах:

```text
GET /api/v1/testing/admin/integrity-reports/
GET /api/v1/testing/admin/integrity-reports/{id}/

GET /api/v1/testing/teacher/integrity-reports/
GET /api/v1/testing/teacher/integrity-reports/{id}/
```

ViewSet:

```text
TestAttemptIntegrityReportViewSet
```

## Payload отчета

`flags_data` должен хранить машинно-читаемые признаки. Рекомендуемый формат элемента:

```json
{
  "code": "fast_completion",
  "label": "Слишком быстрое прохождение",
  "score": 20,
  "details": {
    "duration_seconds": 45
  }
}
```

Правила:

- `code` должен быть стабильным для frontend и аналитики;
- `label` можно показывать преподавателю;
- `score` участвует в расчете общего риска;
- `details` должен быть безопасен для показа преподавателю и не содержать лишних персональных данных.

## Валидация

Валидация отчета находится в:

```text
apps/testing/validators/integrity/report.py
```

Проверяются:

- диапазон `score`;
- соответствие `risk_level`;
- структура `flags_data`;
- наличие связанной попытки.

## Пересчет

Существуют два сценария:

1. Построить payload без сохранения.
2. Построить и сохранить отчет.

Функции:

```text
build_attempt_integrity_report_task
build_and_save_attempt_integrity_report_task
build_attempt_integrity_report_payload
build_and_save_attempt_integrity_report
```

Первый сценарий оставлен для обратной совместимости существующего endpoint/flow. Основной рабочий сценарий после submit - построить и сохранить отчет.

## Использование в проверке

Integrity report должен помогать преподавателю принимать решение, но не должен автоматически блокировать результат без отдельного бизнес-правила.

Рекомендуемый flow:

1. Обучающийся отправляет попытку.
2. Backend выполняет автопроверку.
3. Backend сохраняет integrity report.
4. Преподаватель видит риск в очереди проверки или деталях попытки.
5. Преподаватель вручную подтверждает, корректирует или комментирует результат.

## Тесты

Покрытие:

```text
apps/testing/tests/api/test_integrity_report_api.py
apps/testing/tests/models/test_integrity_models.py
apps/testing/tests/selectors/test_integrity_selectors.py
apps/testing/tests/services/test_integrity_persistence_services.py
apps/testing/tests/services/test_integrity_services.py
apps/testing/tests/validators/test_integrity_validators.py
```

При добавлении новых признаков риска нужно обновлять:

- service расчета;
- validator структуры flags;
- API serializer;
- тесты persistence и API;
- frontend mapping для отображения признаков.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
