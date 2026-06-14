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
# Olympiads Module

## Назначение

Модуль `olympiads` отвечает за проведение олимпиад, конкурсов, хакатонов и проектных мероприятий.

Главная идея:

> **Побеждает знание, а не связи.**

---

## Основные задачи

- создание олимпиады;
- регистрация участников;
- проведение туров;
- выдача заданий;
- приём решений;
- проверка;
- анонимизация;
- апелляции;
- рейтинги;
- дипломы;
- сертификаты;
- протокол результатов.

---

## Основные модели

```text
Olympiad
OlympiadRound
OlympiadTask
OlympiadParticipant
OlympiadSubmission
OlympiadReview
Appeal
OlympiadResult
Certificate
```

---

## Честная проверка

Модуль должен поддерживать анонимизацию работ, критерии оценивания, историю проверки, случайное распределение экспертов, невозможность скрытой подмены результата, апелляции и протокол действий.

---

## API

```text
GET    /api/v1/olympiads/
POST   /api/v1/olympiads/
GET    /api/v1/olympiads/{id}/
POST   /api/v1/olympiads/{id}/register/
GET    /api/v1/olympiads/{id}/rounds/
POST   /api/v1/olympiad-rounds/{id}/submit/
POST   /api/v1/olympiad-submissions/{id}/review/
POST   /api/v1/olympiad-results/{id}/appeal/
GET    /api/v1/olympiads/{id}/results/
```

---

## Важные правила

- нельзя менять результат без истории;
- проверяющий не должен видеть личность участника при анонимной проверке;
- критерии должны быть опубликованы заранее;
- апелляция должна иметь статус и историю.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
