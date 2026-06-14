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
# Commit Convention

## Формат

```text
type(scope): message
```

Примеры:

```text
feat(assignments): add submission review flow
fix(schedule): prevent classroom time conflicts
refactor(courses): split course detail components
docs(vision): update product mission
test(journal): cover grade history
```

---

## Типы

- `feat` — новая функция;
- `fix` — исправление ошибки;
- `refactor` — рефакторинг без изменения поведения;
- `docs` — документация;
- `style` — стили или форматирование;
- `test` — тесты;
- `chore` — технические задачи;
- `ci` — CI/CD.

---

## Scope

Scope указывает модуль: `auth`, `users`, `organizations`, `courses`, `lessons`, `assignments`, `journal`, `schedule`, `analytics`, `ai`, `ui`, `docs`, `infra`.

---

## Правила

Один коммит — одна логическая задача. Не смешивать refactor и feature без необходимости. Не коммитить `.env`, временные файлы и большие бинарные файлы без необходимости.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
