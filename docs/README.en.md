<!-- DLE-Pifagor README Header -->
<p align="center">
  <a href="../README.en.md"><img src="../design/logos/main/pifagor-logo-primary.svg" alt="DLE Pifagor" width="104" /></a>
</p>

<p align="center">
  <strong>DLE "Pifagor"</strong><br />
  <sub>Project documentation and development materials</sub>
</p>

<p align="center">
  <a href="../README.en.md">Project README</a> ·
  <a href="../docs/README.en.md">Documentation</a> ·
  <a href="../README.md">Русская версия</a>
</p>

---
<!-- /DLE-Pifagor README Header -->

# DLE-Pifagor Documentation

This directory contains product, architecture, interface, and engineering documentation for the **DLE-Pifagor** educational platform.

The documentation helps contributors understand why the project exists, how it is structured, which modules are described, and which development rules are used.

## Structure

```text
docs/
├─ 00-vision/          # product idea, mission, positioning, and roadmap
├─ 01-architecture/    # backend, frontend, API, and data architecture
├─ 02-modules/         # functional platform modules
├─ 03-design-system/   # visual and interface principles
├─ 04-development/     # development, testing, git, and deployment rules
├─ decisions/          # architecture decision records
├─ README.md           # Russian documentation navigation
└─ README.en.md        # English documentation navigation
```

## 00-vision

- `product-vision.md` - product vision.
- `mission.md` - project mission and philosophy.
- `positioning.md` - positioning and differences from alternatives.
- `roadmap-after-mvp.md` - development plan after the diploma MVP.

## 01-architecture

- `project-structure.md` - general repository structure.
- `backend-architecture.md` - Django backend architecture.
- `frontend-architecture.md` - Vue frontend architecture.
- `api-architecture.md` - REST API principles and endpoint structure.
- `database-schema.md` - core database entities and relationships.

## 02-modules

- `users.md` - users, roles, and profiles.
- `organizations.md` - educational organizations and user relations.
- `courses.md` - courses, learning materials, lessons, and progress.
- `assignments.md` - assignments, submissions, and review flow.
- `journal.md` - gradebook, grades, and attendance.
- `schedule.md` - schedule, time slots, and replacements.
- `calendar-and-notes.md` - calendar, daily plan, and personal notes.
- `notifications.md` - notifications, counters, and user preferences.
- `feedback.md` - user requests, attachments, and admin handling.
- `settings.md` - appearance, notification, privacy, role, and security settings.
- `ai-anastasia.md` - AI assistant Anastasia.
- `olympiads.md` - olympiads, contests, and transparent evaluation.

## 03-design-system

- `ui-principles.md` - core interface principles.
- `colors.md` - color system.
- `typography.md` - typography and UI text tone.
- `components.md` - base UI components.
- `age-themes.md` - age-based interface themes.

## 04-development

- `coding-rules.md` - coding rules.
- `commit-convention.md` - commit message convention.
- `git-workflow.md` - branch workflow.
- `testing-strategy.md` - testing strategy.
- `deployment.md` - basic deployment principles.

## decisions

- `0001-use-modular-monolith.md` - decision to use a modular monolith.
- `0002-use-vue-and-django.md` - decision to use Vue and Django.
- `0003-role-system.md` - decision on the flexible role system.
- `0004-age-based-interface-themes.md` - decision on age-based interface themes.

## Recommended reading order

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

## Maintenance rules

When a new functional module is added, update:

- the relevant file in `02-modules/`;
- this index and `README.md`;
- architecture documents if layers, API, or data models changed;
- an ADR in `decisions/` if a notable architecture decision was made.
---
---
---

<!-- DLE-Pifagor README Footer -->
---

<p align="center">
  <sub>DLE "Pifagor" · unified digital learning environment</sub>
</p>

<p align="center">
  <a href="../README.en.md">Project README</a> ·
  <a href="../docs/README.en.md">Documentation</a> ·
  <a href="../README.md">Русская версия</a>
</p>
<!-- /DLE-Pifagor README Footer -->
