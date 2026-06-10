<!-- DLE-Pifagor Root Header -->
<p align="center">
  <a href="README.en.md"><img src="design/logos/main/pifagor-logo-primary.svg" alt="DLE Pifagor" width="104" /></a>
</p>

<p align="center">
  <strong>DLE "Pifagor"</strong><br />
  <sub>Project root documentation · Contributing Guide</sub>
</p>

<p align="center">
  <a href="README.en.md">Project README</a> ·
  <a href="docs/README.en.md">Documentation</a> ·
  <a href="CONTRIBUTING.md">Русская версия</a>
</p>

---
<!-- /DLE-Pifagor Root Header -->

# Contributing Guide

## General rules

DLE "Pifagor" is maintained as a modular educational platform. Changes should preserve the current structure: logic belongs to composables/services, UI text belongs to data files, transformations belong to mappers, types belong to types, and pages should stay thin.

## Branches

Use short descriptive branch names:

- `feat/<module>-<task>` for new features.
- `fix/<module>-<bug>` for fixes.
- `refactor/<module>-<scope>` for refactoring.
- `docs/<topic>` for documentation.

## Commits

Commit format:

```text
<type>(<scope>): <description>
```

Examples:

```text
feat(frontend): Add notes page
fix(backend): Fix notification delivery
refactor(docs): Update README structure
```

## Before a pull request

Before submitting changes, check that:

- frontend builds and passes type-check;
- backend passes check, migrations check, ruff, black, and isort;
- documentation is updated together with API, route, and model changes;
- new components do not duplicate existing shared components;
- sensitive data is not committed.

## Frontend structure

Each module should follow this layout:

- `api` - low-level requests;
- `services` - backend-facing workflows;
- `mappers` - DTO to UI-model transformations;
- `types` - types and interfaces;
- `data` - texts, labels, options;
- `composables` - state and user scenarios;
- `components` - presentational components;
- `pages` - thin pages.

## Backend structure

The backend is split into Django apps. Large files should be decomposed into `serializers`, `views`, `selectors`, `services`, and `tests` packages when they become hard to maintain.

## Documentation

If a change adds behavior, an endpoint, a setting, a workflow, or a constraint, update the matching file in `docs/`.

<!-- DLE-Pifagor Root Footer -->
---

<p align="center">
  <sub>DLE "Pifagor" · unified digital learning environment</sub>
</p>

<p align="center">
  <a href="README.en.md">Project README</a> ·
  <a href="docs/README.en.md">Documentation</a> ·
  <a href="CONTRIBUTING.md">Русская версия</a>
</p>
<!-- /DLE-Pifagor Root Footer -->
