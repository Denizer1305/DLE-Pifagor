# Документация ЦОС «Пифагор»

Добро пожаловать в документацию проекта **Цифровая образовательная среда «Пифагор»**.

**ЦОС «Пифагор»** — это единая цифровая экосистема для обучения, наставничества, проектной деятельности, аналитики и формирования честных образовательных данных.

Документация описывает продуктовую идею, архитектуру, модули, дизайн-систему, правила разработки и ключевые архитектурные решения проекта.

---

## Структура документации

```text
docs/
 ┣ 00-vision/
 ┣ 01-architecture/
 ┣ 02-modules/
 ┣ 03-design-system/
 ┣ 04-development/
 ┣ decisions/
 ┣ README.md
 ┗ README.en.md
```

---

## 00-vision

Раздел описывает видение продукта, миссию, позиционирование и дорожную карту после MVP.

```text
00-vision/
 ┣ mission.md
 ┣ positioning.md
 ┣ product-vision.md
 ┗ roadmap-after-mvp.md
```

### Файлы

- `product-vision.md` — основное видение ЦОС «Пифагор».
- `mission.md` — миссия проекта и философия среды.
- `positioning.md` — позиционирование продукта и отличие от аналогов.
- `roadmap-after-mvp.md` — план развития после дипломного MVP.

---

## 01-architecture

Раздел описывает техническую архитектуру проекта.

```text
01-architecture/
 ┣ api-architecture.md
 ┣ backend-architecture.md
 ┣ database-schema.md
 ┣ frontend-architecture.md
 ┗ project-structure.md
```

### Файлы

- `project-structure.md` — общая структура репозитория.
- `backend-architecture.md` — архитектура backend на Django.
- `frontend-architecture.md` — архитектура frontend на Vue.
- `api-architecture.md` — принципы REST API и структура endpoints.
- `database-schema.md` — основные сущности базы данных и связи.

---

## 02-modules

Раздел описывает крупные продуктовые и технические модули платформы.

```text
02-modules/
 ┣ ai-anastasia.md
 ┣ assignments.md
 ┣ courses.md
 ┣ journal.md
 ┣ lessons.md
 ┣ olympiads.md
 ┣ organizations.md
 ┣ schedule.md
 ┗ users.md
```

### Файлы

- `users.md` — пользователи, роли и профили.
- `organizations.md` — образовательные организации, группы и учебные периоды.
- `courses.md` — курсы и дисциплины.
- `lessons.md` — цифровые уроки и структура занятия.
- `assignments.md` — задания, сдача работ и проверка.
- `journal.md` — электронный журнал, оценки и посещаемость.
- `schedule.md` — расписание, кабинеты, временные слоты и замены.
- `ai-anastasia.md` — ИИ-помощник «Анастасия».
- `olympiads.md` — олимпиады, конкурсы и честная проверка.

---

## 03-design-system

Раздел описывает визуальные и интерфейсные принципы платформы.

```text
03-design-system/
 ┣ age-themes.md
 ┣ colors.md
 ┣ components.md
 ┣ typography.md
 ┗ ui-principles.md
```

### Файлы

- `ui-principles.md` — основные принципы интерфейса.
- `colors.md` — цветовая система.
- `typography.md` — типографика и тон текстов.
- `components.md` — базовые UI-компоненты.
- `age-themes.md` — возрастные темы интерфейса: младшие, средние, старшие классы, колледж и университет.

---

## 04-development

Раздел описывает правила разработки и сопровождения проекта.

```text
04-development/
 ┣ coding-rules.md
 ┣ commit-convention.md
 ┣ deployment.md
 ┣ git-workflow.md
 ┗ testing-strategy.md
```

### Файлы

- `coding-rules.md` — правила написания кода.
- `commit-convention.md` — соглашение о коммитах.
- `git-workflow.md` — процесс работы с ветками.
- `testing-strategy.md` — стратегия тестирования.
- `deployment.md` — базовые принципы развёртывания.

---

## decisions

Раздел содержит архитектурные решения в формате ADR.

```text
decisions/
 ┣ 0001-use-modular-monolith.md
 ┣ 0002-use-vue-and-django.md
 ┣ 0003-role-system.md
 ┗ 0004-age-based-interface-themes.md
```

### Файлы

- `0001-use-modular-monolith.md` — решение использовать модульный монолит.
- `0002-use-vue-and-django.md` — решение использовать Vue и Django.
- `0003-role-system.md` — решение о гибкой ролевой системе.
- `0004-age-based-interface-themes.md` — решение о возрастных темах интерфейса.

---

## Основные идеи проекта

ЦОС «Пифагор» строится вокруг нескольких ключевых принципов:

- единая цифровая среда вместо набора разрозненных сервисов;
- преподаватель освобождается от рутины и становится наставником;
- ученик развивается по индивидуальной траектории;
- родитель получает спокойную и понятную картину обучения;
- образовательная организация видит честные данные;
- ИИ-помощник «Анастасия» усиливает человека, а не заменяет его;
- данные используются для развития, а не для давления.

---

## Рекомендуемый порядок чтения

Если вы знакомитесь с проектом впервые, лучше читать документацию в таком порядке:

1. `00-vision/product-vision.md`
2. `00-vision/mission.md`
3. `00-vision/positioning.md`
4. `01-architecture/project-structure.md`
5. `01-architecture/backend-architecture.md`
6. `01-architecture/frontend-architecture.md`
7. `02-modules/users.md`
8. `02-modules/courses.md`
9. `02-modules/lessons.md`
10. `02-modules/assignments.md`
11. `02-modules/journal.md`
12. `04-development/coding-rules.md`

---

## Навигация для разработчика

### Хочу понять архитектуру

Начните с:

- `01-architecture/project-structure.md`
- `01-architecture/backend-architecture.md`
- `01-architecture/frontend-architecture.md`
- `01-architecture/api-architecture.md`

### Хочу понять продукт

Начните с:

- `00-vision/product-vision.md`
- `00-vision/mission.md`
- `00-vision/positioning.md`

### Хочу понять модули

Начните с:

- `02-modules/users.md`
- `02-modules/organizations.md`
- `02-modules/courses.md`
- `02-modules/lessons.md`
- `02-modules/assignments.md`

### Хочу понять стиль интерфейса

Начните с:

- `03-design-system/ui-principles.md`
- `03-design-system/colors.md`
- `03-design-system/components.md`
- `03-design-system/age-themes.md`

### Хочу понять правила разработки

Начните с:

- `04-development/coding-rules.md`
- `04-development/git-workflow.md`
- `04-development/commit-convention.md`
- `04-development/testing-strategy.md`

---

## Статус документации

Документация находится в стадии активного развития.

По мере роста проекта в неё нужно добавлять:

- новые модули;
- новые архитектурные решения;
- схемы API;
- ER-диаграммы;
- UI-гайды;
- сценарии пользователей;
- инструкции по развёртыванию;
- правила безопасности.

---

## Девиз проекта

> **Человек рождён, чтобы мечтать и созидать великое.**

---

## Идентичность

**Сделано во Владимире.**

**Создано для России.**
