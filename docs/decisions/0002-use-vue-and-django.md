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
# ADR 0002: Use Vue and Django

## Status

Accepted

## Context

Проект ЦОС «Пифагор» требует сложного ролевого интерфейса, личных кабинетов, карточек, таблиц, форм, дашбордов, большого количества связанных сущностей и надёжного backend.

---

## Decision

Использовать стек:

```text
Frontend: Vue 3 + TypeScript + Vite
Backend: Django + Django REST Framework
Database: PostgreSQL
```

---

## Reasons

Vue хорошо подходит для компонентных интерфейсов и уже используется в проекте. Django подходит для систем с большим количеством моделей, ролей и прав доступа. DRF удобен для REST API. PostgreSQL подходит для сложной реляционной модели.

---

## Consequences

Плюсы: понятный стек, быстрый рост, хорошая поддержка, подходит для MVP и продукта.

Минусы: нужно следить за структурой frontend, не перегружать Django views бизнес-логикой и заранее продумать права доступа.
---
---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
