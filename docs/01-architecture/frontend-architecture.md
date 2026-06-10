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
# Frontend Architecture

## Общий подход

Frontend ЦОС «Пифагор» строится как модульное Vue-приложение.

Основной стек: Vue 3, TypeScript, Vite, Vue Router, Pinia, Axios, SCSS или CSS Modules, собственная дизайн-система.

---

## Общая структура frontend

```text
frontend/
 ┣ public/
 ┣ src/
 ┃ ┣ app/
 ┃ ┣ assets/
 ┃ ┣ components/
 ┃ ┣ layouts/
 ┃ ┣ modules/
 ┃ ┣ pages/
 ┃ ┣ router/
 ┃ ┣ stores/
 ┃ ┣ services/
 ┃ ┣ composables/
 ┃ ┣ styles/
 ┃ ┣ utils/
 ┃ ┣ types/
 ┃ ┗ main.ts
 ┣ index.html
 ┣ vite.config.ts
 ┣ tsconfig.json
 ┗ package.json
```

---

## `app/`

Глобальная настройка приложения: провайдеры, настройки API, роли, маршруты и глобальные константы.

```text
app/
 ┣ App.vue
 ┣ providers/
 ┣ config/
 ┗ constants/
```

---

## `components/`

Общие переиспользуемые компоненты.

```text
components/
 ┣ base/
 ┣ dashboard/
 ┣ navigation/
 ┣ forms/
 ┣ charts/
 ┣ modals/
 ┗ icons/
```

`base/` содержит `BaseButton`, `BaseInput`, `BaseSelect`, `BaseModal`, `BaseCard`, `BaseBadge`, `BaseAvatar`, `BaseProgress`, `BaseTabs`, `BaseTable`, `BaseEmptyState`.

`dashboard/` содержит `DashboardHero`, `StatsCard`, `ScheduleCard`, `AssignmentCard`, `ProgressCard`, `AiAssistantCard`, `ActivityFeed`.

---

## `layouts/`

```text
layouts/
 ┣ MainLayout.vue
 ┣ AuthLayout.vue
 ┣ CabinetLayout.vue
 ┣ StudentLayout.vue
 ┣ ParentLayout.vue
 ┣ TeacherLayout.vue
 ┣ AdminLayout.vue
 ┗ PublicLayout.vue
```

Layout отвечает за общую структуру страницы: sidebar, header, рабочую область, адаптивность и слоты.

---

## `modules/`

Главная зона разработки.

```text
modules/
 ┣ auth/
 ┣ users/
 ┣ organizations/
 ┣ student/
 ┣ parent/
 ┣ teacher/
 ┣ admin/
 ┣ courses/
 ┣ lessons/
 ┣ assignments/
 ┣ testing/
 ┣ journal/
 ┣ schedule/
 ┣ materials/
 ┣ notifications/
 ┣ analytics/
 ┣ achievements/
 ┣ portfolio/
 ┣ projects/
 ┣ olympiads/
 ┣ ai/
 ┗ settings/
```

Модуль содержит всё, что относится к предметной области: `api`, `components`, `composables`, `pages`, `stores`, `types`, `utils`, `index.ts`.

---

## `router/`

```text
router/
 ┣ index.ts
 ┣ public.routes.ts
 ┣ auth.routes.ts
 ┣ student.routes.ts
 ┣ parent.routes.ts
 ┣ teacher.routes.ts
 ┣ admin.routes.ts
 ┣ course.routes.ts
 ┣ journal.routes.ts
 ┗ guards.ts
```

В `guards.ts` должны быть проверки авторизации, роли, доступа к организации и профиля пользователя.

---

## Принцип компонентизации

Компонент должен отвечать за одну задачу. Если компонент становится слишком большим, его нужно разделить на visual components, container components, composables и service functions.

Рекомендуемый размер: базовый компонент до 150 строк, обычный компонент до 300 строк, страница до 400 строк.

---

## Возрастные интерфейсы

Пифагор поддерживает идею, что интерфейс взрослеет вместе с учеником: `junior`, `middle`, `senior`, `college`, `university`.

Тема может влиять на логотип, цвета, иллюстрации, плотность интерфейса, тексты, стиль карточек и уровень игровизации.
---
---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
