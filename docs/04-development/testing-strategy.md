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
# Testing Strategy

## Цель

Тесты нужны не ради процента покрытия, а чтобы основные сценарии ЦОС «Пифагор» не ломались при развитии проекта.

---

## Уровни

- Unit tests — отдельные функции и сервисы.
- Integration tests — взаимодействие модулей.
- API tests — endpoints и права доступа.
- Frontend tests — компоненты и composables.
- E2E tests — сценарий целиком.

---

## Backend tools

- pytest;
- pytest-django;
- factory_boy;
- coverage.

---

## Frontend tools

- Vitest;
- Vue Test Utils;
- Playwright для E2E.

---

## Критичные сценарии

- вход в систему;
- проверка роли;
- запрет доступа к чужим данным;
- создание задания;
- сдача работы;
- проверка работы;
- выставление оценки;
- история изменения оценки;
- конфликт расписания;
- родитель видит только своих детей.

---

## Главный принцип

> Сначала тестировать права доступа и жизненно важные образовательные сценарии.
---
---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
