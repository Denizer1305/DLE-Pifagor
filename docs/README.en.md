# DLE “Pifagor” Documentation

Welcome to the documentation of **Digital Learning Environment “Pifagor”**.

**DLE “Pifagor”** is a unified digital ecosystem for learning, mentoring, project-based work, analytics, and honest educational data.

This documentation describes the product vision, architecture, modules, design system, development rules, and key architectural decisions of the project.

---

## Documentation Structure

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

This section describes the product vision, mission, positioning, and post-MVP roadmap.

```text
00-vision/
 ┣ mission.md
 ┣ positioning.md
 ┣ product-vision.md
 ┗ roadmap-after-mvp.md
```

### Files

- `product-vision.md` — the main product vision of DLE “Pifagor”.
- `mission.md` — the mission and philosophy of the environment.
- `positioning.md` — product positioning and differences from alternatives.
- `roadmap-after-mvp.md` — development plan after the diploma MVP.

---

## 01-architecture

This section describes the technical architecture of the project.

```text
01-architecture/
 ┣ api-architecture.md
 ┣ backend-architecture.md
 ┣ database-schema.md
 ┣ frontend-architecture.md
 ┗ project-structure.md
```

### Files

- `project-structure.md` — general repository structure.
- `backend-architecture.md` — backend architecture based on Django.
- `frontend-architecture.md` — frontend architecture based on Vue.
- `api-architecture.md` — REST API principles and endpoint structure.
- `database-schema.md` — main database entities and relationships.

---

## 02-modules

This section describes the main product and technical modules of the platform.

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

### Files

- `users.md` — users, roles, and profiles.
- `organizations.md` — educational organizations, groups, and academic periods.
- `courses.md` — courses and disciplines.
- `lessons.md` — digital lessons and lesson structure.
- `assignments.md` — assignments, submissions, and review flow.
- `journal.md` — electronic journal, grades, and attendance.
- `schedule.md` — schedule, classrooms, time slots, and replacements.
- `ai-anastasia.md` — AI assistant “Anastasia”.
- `olympiads.md` — olympiads, contests, and transparent evaluation.

---

## 03-design-system

This section describes the visual and interface principles of the platform.

```text
03-design-system/
 ┣ age-themes.md
 ┣ colors.md
 ┣ components.md
 ┣ typography.md
 ┗ ui-principles.md
```

### Files

- `ui-principles.md` — core interface principles.
- `colors.md` — color system.
- `typography.md` — typography and UI text tone.
- `components.md` — base UI components.
- `age-themes.md` — age-based interface themes: junior, middle, senior, college, and university.

---

## 04-development

This section describes development and maintenance rules.

```text
04-development/
 ┣ coding-rules.md
 ┣ commit-convention.md
 ┣ deployment.md
 ┣ git-workflow.md
 ┗ testing-strategy.md
```

### Files

- `coding-rules.md` — coding rules.
- `commit-convention.md` — commit message convention.
- `git-workflow.md` — branch workflow.
- `testing-strategy.md` — testing strategy.
- `deployment.md` — basic deployment principles.

---

## decisions

This section contains architecture decision records.

```text
decisions/
 ┣ 0001-use-modular-monolith.md
 ┣ 0002-use-vue-and-django.md
 ┣ 0003-role-system.md
 ┗ 0004-age-based-interface-themes.md
```

### Files

- `0001-use-modular-monolith.md` — decision to use a modular monolith.
- `0002-use-vue-and-django.md` — decision to use Vue and Django.
- `0003-role-system.md` — decision on the flexible role system.
- `0004-age-based-interface-themes.md` — decision on age-based interface themes.

---

## Core Project Ideas

DLE “Pifagor” is built around several key principles:

- one unified digital environment instead of disconnected services;
- teachers are freed from routine work and become mentors;
- students grow along an individual educational path;
- parents receive a calm and clear view of the learning process;
- educational organizations see honest data;
- AI assistant “Anastasia” strengthens people instead of replacing them;
- data is used for development, not pressure.

---

## Recommended Reading Order

If you are new to the project, read the documentation in this order:

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

## Navigation for Developers

### I want to understand the architecture

Start with:

- `01-architecture/project-structure.md`
- `01-architecture/backend-architecture.md`
- `01-architecture/frontend-architecture.md`
- `01-architecture/api-architecture.md`

### I want to understand the product

Start with:

- `00-vision/product-vision.md`
- `00-vision/mission.md`
- `00-vision/positioning.md`

### I want to understand the modules

Start with:

- `02-modules/users.md`
- `02-modules/organizations.md`
- `02-modules/courses.md`
- `02-modules/lessons.md`
- `02-modules/assignments.md`

### I want to understand the interface style

Start with:

- `03-design-system/ui-principles.md`
- `03-design-system/colors.md`
- `03-design-system/components.md`
- `03-design-system/age-themes.md`

### I want to understand development rules

Start with:

- `04-development/coding-rules.md`
- `04-development/git-workflow.md`
- `04-development/commit-convention.md`
- `04-development/testing-strategy.md`

---

## Documentation Status

This documentation is under active development.

As the project grows, it should be expanded with:

- new modules;
- new architecture decisions;
- API schemas;
- ER diagrams;
- UI guides;
- user scenarios;
- deployment instructions;
- security rules.

---

## Project Motto

> **A human is born to dream and create something great.**

---

## Identity

**Made in Vladimir.**

**Created for Russia.**
