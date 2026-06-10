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

# Документация DLE-Pifagor

Эта папка содержит продуктовую, архитектурную, интерфейсную и инженерную документацию образовательной платформы **DLE-Pifagor**.

Документация помогает быстро понять, зачем существует проект, как он устроен, какие модули уже описаны и какие правила используются при разработке.

## Структура

```text
docs/
├─ 00-vision/          # продуктовая идея, миссия, позиционирование и roadmap
├─ 01-architecture/    # архитектура backend, frontend, API и данных
├─ 02-modules/         # описание функциональных модулей платформы
├─ 03-design-system/   # визуальные и интерфейсные принципы
├─ 04-development/     # правила разработки, тестирования, git и deployment
├─ decisions/          # архитектурные решения в формате ADR
├─ README.md           # русская навигация по документации
└─ README.en.md        # английская навигация по документации
```

## 00-vision

- `product-vision.md` - продуктовое видение платформы.
- `mission.md` - миссия и философия проекта.
- `positioning.md` - позиционирование и отличие от альтернатив.
- `roadmap-after-mvp.md` - план развития после дипломного MVP.

## 01-architecture

- `project-structure.md` - общая структура репозитория.
- `backend-architecture.md` - архитектура backend на Django.
- `frontend-architecture.md` - архитектура frontend на Vue.
- `api-architecture.md` - принципы REST API и структура endpoints.
- `database-schema.md` - ключевые сущности базы данных и связи.

## 02-modules

- `users.md` - пользователи, роли и профили.
- `organizations.md` - образовательные организации и связи с пользователями.
- `courses.md` - курсы, учебные материалы, занятия и прогресс.
- `assignments.md` - задания, сдача работ и проверка.
- `journal.md` - электронный журнал, оценки и посещаемость.
- `schedule.md` - расписание, слоты и замены.
- `calendar-and-notes.md` - календарь, план на день и личные заметки.
- `notifications.md` - уведомления, счетчики и пользовательские настройки.
- `feedback.md` - обращения пользователей, вложения и администрирование заявок.
- `settings.md` - настройки внешнего вида, уведомлений, приватности, ролей и безопасности.
- `ai-anastasia.md` - ИИ-помощник «Анастасия».
- `olympiads.md` - олимпиады, конкурсы и прозрачная проверка.

## 03-design-system

- `ui-principles.md` - базовые принципы интерфейса.
- `colors.md` - цветовая система.
- `typography.md` - типографика и тон текстов.
- `components.md` - базовые UI-компоненты.
- `age-themes.md` - возрастные темы интерфейса.

## 04-development

- `coding-rules.md` - правила написания кода.
- `commit-convention.md` - соглашение о коммитах.
- `git-workflow.md` - процесс работы с ветками.
- `testing-strategy.md` - стратегия тестирования.
- `deployment.md` - базовые принципы развертывания.

## decisions

- `0001-use-modular-monolith.md` - решение использовать модульный монолит.
- `0002-use-vue-and-django.md` - решение использовать Vue и Django.
- `0003-role-system.md` - решение о гибкой ролевой системе.
- `0004-age-based-interface-themes.md` - решение о возрастных темах интерфейса.

## Рекомендуемый порядок чтения

1. `00-vision/product-vision.md`
2. `00-vision/mission.md`
3. `01-architecture/project-structure.md`
4. `01-architecture/backend-architecture.md`
5. `01-architecture/frontend-architecture.md`
6. `02-modules/users.md`
7. `02-modules/organizations.md`
8. `02-modules/courses.md`
9. `02-modules/calendar-and-notes.md`
10. `02-modules/notifications.md`
11. `02-modules/feedback.md`
12. `04-development/coding-rules.md`

## Поддержание порядка

При добавлении нового функционального модуля обновляйте:

- соответствующий файл в `02-modules/`;
- этот индекс и `README.en.md`;
- архитектурные документы, если меняются слои, API или модель данных;
- ADR в `decisions/`, если принято заметное архитектурное решение.
---
---
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
