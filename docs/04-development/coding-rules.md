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
# Coding Rules

## Общие правила

Код ЦОС «Пифагор» должен быть понятным, поддерживаемым и готовым к росту проекта.

Главный принцип: лучше несколько понятных файлов, чем один огромный файл на тысячу строк.

---

## Backend

Каждый модуль должен быть отдельным Django app. View не должен содержать бизнес-логику. Бизнес-логику выносить в `services.py`. Сложные выборки выносить в `selectors.py`. Права доступа описывать в `permissions.py`. Доменные проверки выносить в `validators.py`.

---

## Frontend

API-запросы не писать в компонентах. Страницы должны собирать компоненты, а не содержать всю логику. Сложную логику выносить в composables и services.

---

## Размер файлов

- Vue base component: до 150 строк;
- обычный Vue component: до 300 строк;
- Vue page: до 400 строк;
- Django service file: до 400 строк;
- CSS/SCSS file: до 400 строк.

Если файл растёт — нужно декомпозировать.

---

## Именование

Компоненты: `AssignmentCard.vue`, `ScheduleCard.vue`, `StudentDashboardPage.vue`.

Composables: `useAssignments.ts`, `useStudentProgress.ts`.

Stores: `assignments.store.ts`, `auth.store.ts`.

---

## Главный принцип

> Код должен быть написан так, чтобы через месяц его можно было понять без археологии.
---
---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
