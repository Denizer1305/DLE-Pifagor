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
# Components

## Назначение

Этот документ описывает базовые компоненты дизайн-системы ЦОС «Пифагор».

Компоненты должны быть переиспользуемыми, понятными и единообразными во всех модулях платформы.

---

## Базовые компоненты

- `BaseButton` — кнопка действия.
- `BaseCard` — базовая карточка.
- `BaseBadge` — метка статуса.
- `BaseInput` — поле ввода.
- `BaseModal` — модальное окно.
- `BaseEmptyState` — пустое состояние.
- `BaseAvatar` — аватар пользователя.
- `BaseProgress` — прогресс.
- `BaseTabs` — вкладки.
- `BaseTable` — таблица.

---

## Dashboard-компоненты

- `DashboardHero` — приветственный блок кабинета.
- `StatsCard` — карточка статистики.
- `ScheduleCard` — карточка расписания.
- `AssignmentCard` — карточка задания.
- `ProgressCard` — карточка прогресса.
- `AiAssistantCard` — карточка помощника «Анастасия».

---

## Навигационные компоненты

- `AppSidebar` — боковая навигация.
- `AppHeader` — верхняя панель.
- `Breadcrumbs` — путь страницы.
- `MobileNavigation` — мобильная навигация.

---

## Правила компонентов

- компонент не должен знать больше, чем ему нужно;
- API-запросы не писать внутри visual components;
- сложную логику выносить в composables;
- loading/error/empty состояния должны быть предусмотрены;
- компонент должен быть доступен с клавиатуры там, где это возможно.

---

## Главный принцип

> Компонент должен решать одну задачу и быть понятным без изучения всего проекта.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
