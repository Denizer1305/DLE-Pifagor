<!-- DLE-Pifagor README Header -->
<p align="center">
  <a href="../README.md"><img src="../design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Документация проекта и материалы разработки</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor README Header -->

# Конфигурации GitHub

Папка содержит настройки GitHub для репозитория DLE-Pifagor: CI-пайплайны, проверки качества и вспомогательные файлы для автоматизации разработки.

## Структура

- `workflows/backend-ci.yml` - проверяет backend: системные проверки Django, миграции, линтеры, форматирование и тесты.
- `workflows/frontend-ci.yml` - проверяет frontend: установку зависимостей, TypeScript, сборку и статические проверки.

## Назначение

Файлы из этой директории помогают удерживать единый стандарт качества перед слиянием изменений. Основная идея простая: каждая часть платформы должна проходить независимую проверку, чтобы ошибки backend и frontend не смешивались в одном пайплайне.

## Когда обновлять

Обновляйте файлы в `.github`, если:

- изменились команды запуска тестов или линтеров;
- добавился новый обязательный этап проверки;
- изменилась структура backend, frontend или requirements;
- нужно настроить отдельные проверки для новых модулей платформы.

## Локальная проверка

Перед push желательно запускать те же команды, которые используются в workflow. Основные команды описаны в корневом `README.md`, а также в `backend/README.md` и `frontend/README.md`.
---

<!-- DLE-Pifagor README Footer -->
---

<p align="center">
  <sub>ЦОС "Пифагор" · единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>
<!-- /DLE-Pifagor README Footer -->
