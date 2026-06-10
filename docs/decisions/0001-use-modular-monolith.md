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
# ADR 0001: Use Modular Monolith

## Status

Accepted

## Context

ЦОС «Пифагор» включает много связанных доменных областей: пользователи, роли, организации, курсы, уроки, задания, журнал, расписание, аналитика, ИИ и олимпиады.

На раннем этапе проект развивается как личный продукт после дипломного MVP.

---

## Decision

Использовать **модульный монолит** на Django.

Каждый предметный модуль оформляется как отдельное Django app, но всё приложение разворачивается как единый backend.

---

## Reasons

- проще разрабатывать одному;
- проще тестировать;
- проще разворачивать;
- проще поддерживать транзакции;
- меньше инфраструктурной сложности;
- можно позже вынести отдельные модули в сервисы.

---

## Consequences

Плюсы: быстрый старт, единая кодовая база, простая отладка, меньше DevOps-нагрузки.

Минусы: нужно следить за границами модулей и не превращать проект в монолитную кашу.
---
---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
