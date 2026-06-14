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
# ADR 0003: Role System

## Status

Accepted

## Context

В ЦОС «Пифагор» пользователь может иметь разные роли: ученик, родитель, преподаватель, куратор, методист, директор, администратор.

Один человек может совмещать несколько ролей.

---

## Decision

Не хранить роль одним полем в `User`.

Использовать отдельные сущности:

```text
User
Role
UserRole
OrganizationMembership
```

---

## Reasons

Такой подход позволяет назначать несколько ролей одному пользователю, учитывать организацию, гибко проверять доступ, развивать систему без переписывания модели пользователя и поддерживать сложные сценарии.

---

## Rule

Любая проверка доступа должна учитывать пользователя, роль, организацию и объект доступа.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
