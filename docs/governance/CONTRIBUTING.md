<!-- DLE-Pifagor Root Header -->
<p align="center">
  <a href="README.md"><img src="design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Корневая документация проекта · Руководство участника проекта</sub>
</p>

<p align="center">
  <a href="README.md">README проекта</a> ·
  <a href="docs/README.md">Документация</a> ·
  <a href="CONTRIBUTING.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor Root Header -->

# Руководство участника проекта

## Общие правила

Проект ЦОС "Пифагор" ведется как модульная образовательная платформа. Любые изменения должны сохранять текущую структуру: логика в composables/services, тексты в data, преобразования в mappers, типы в types, а страницы остаются тонкими.

## Ветки

Используйте короткие осмысленные имена веток:

- `feat/<module>-<task>` для новой функциональности.
- `fix/<module>-<bug>` для исправлений.
- `refactor/<module>-<scope>` для рефакторинга.
- `docs/<topic>` для документации.

## Коммиты

Формат коммита:

```text
<type>(<scope>): <описание>
```

Примеры:

```text
feat(frontend): Добавлена страница заметок
fix(backend): Исправлена выдача уведомлений
refactor(docs): Обновлена структура README
```

## Перед pull request

Перед отправкой изменений проверьте:

- frontend собирается и проходит type-check;
- backend проходит check, migrations check, ruff, black и isort;
- документация обновлена вместе с изменениями API, маршрутов и моделей;
- новые компоненты не дублируют существующие общие компоненты;
- чувствительные данные не попали в репозиторий.

## Структура frontend

Каждый модуль должен придерживаться схемы:

- `api` - низкоуровневые запросы;
- `services` - сценарии работы с backend;
- `mappers` - преобразование DTO в UI-модели;
- `types` - типы и интерфейсы;
- `data` - тексты, labels, опции;
- `composables` - состояние и пользовательские сценарии;
- `components` - тупые компоненты;
- `pages` - тонкие страницы.

## Структура backend

Backend делится по приложениям Django. Крупные файлы нужно декомпозировать по папкам `serializers`, `views`, `selectors`, `services`, `tests`, если файл становится трудно поддерживать.

## Документация

Если изменение добавляет поведение, endpoint, настройку, workflow или ограничение, обновите соответствующий файл в `docs/`.

<!-- DLE-Pifagor Root Footer -->
---

<p align="center">
  <sub>ЦОС "Пифагор" · единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="README.md">README проекта</a> ·
  <a href="docs/README.md">Документация</a> ·
  <a href="CONTRIBUTING.en.md">English version</a>
</p>
<!-- /DLE-Pifagor Root Footer -->
