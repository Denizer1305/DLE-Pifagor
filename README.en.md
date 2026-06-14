<!-- DLE-Pifagor Root Header -->
<p align="center">
  <a href="README.en.md"><img src="design/logos/main/pifagor-logo-primary.svg" alt="DLE Pifagor" width="104" /></a>
</p>

<p align="center">
  <strong>DLE "Pifagor"</strong><br />
  <sub>Project root documentation · Project README</sub>
</p>

<p align="center">
  <a href="README.en.md">Project README</a> ·
  <a href="docs/README.en.md">Documentation</a> ·
  <a href="README.md">Русская версия</a>
</p>

---
<!-- /DLE-Pifagor Root Header -->

## About

**DLE-Pifagor** is a diploma educational platform that combines a public website, authentication, administrator, teacher, student and parent dashboards, user management, educational organizations, calendar, notes, notifications, feedback requests, and settings.

The project is designed as a unified digital learning environment: the backend owns domain models, API, permissions, notifications, and data processing, while the frontend provides role-based workspaces with a consistent design system.

## Quick links

| Section | Link |
| --- | --- |
| Documentation | [`docs/README.en.md`](docs/README.en.md) |
| Backend | [`backend/README.en.md`](backend/README.en.md) |
| Frontend | [`frontend/README.md`](frontend/README.md) |
| Design and logos | [`design/README.md`](design/README.md) |
| Infrastructure | [`infra/README.en.md`](infra/README.en.md) |
| Scripts | [`scripts/README.en.md`](scripts/README.en.md) |
| GitHub Actions | [`.github/README.en.md`](.github/README.en.md) |
| API architecture | [`docs/01-architecture/api-architecture.md`](docs/01-architecture/api-architecture.md) |
| Platform modules | [`docs/02-modules/`](docs/02-modules/) |
| Coding rules | [`docs/04-development/coding-rules.md`](docs/04-development/coding-rules.md) |
| Governance documents | [`docs/governance/`](docs/governance/) |

## Stack

### Backend

- Python 3.12+
- Django 5
- Django REST Framework
- PostgreSQL
- Redis and Celery for background jobs
- django-filter
- drf-spectacular
- Ruff, Black, isort
- Django tests, coverage, GitHub Actions

### Frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- Font Awesome
- CSS split by feature/domain

### Infrastructure and quality

- GitHub Actions
- Direct backend checks with Django, Ruff, Black, and isort
- Separate backend and frontend CI workflows
- Documentation for modules, architecture, and decisions

## Implemented areas

- Public pages: home, about, teachers, contacts.
- Authentication: login, registration, email verification, password recovery, logout.
- Dashboards: administrator, teacher, student, parent.
- User profile: view, edit, avatar, contacts, city, privacy.
- Settings: appearance, themes, language, notifications, privacy, roles, security.
- User administration: list, filters, create, detail, edit.
- Organizations: organizations, departments, groups, subjects, teachers, curators, join requests, codes.
- Calendar and notes: events, daily plan, notes on calendar, dedicated notes page.
- Notifications: counters, dropdown, notification page, notification preferences.
- Feedback: user form, attachments, notifications, admin handling.
- Error pages and technical placeholders in the platform style.

## Repository structure

```text
DLE-Pifagor/
├─ .github/          # GitHub Actions and repository settings
├─ backend/          # Django backend and API
├─ design/           # brand, logos, presentations, and visual assets
├─ docs/             # architecture, modules, design system, ADR
├─ frontend/         # Vue frontend
├─ infra/            # Docker, nginx, deployment, and operational notes
├─ scripts/          # project utilities
├─ README.md         # Russian version
└─ README.en.md      # English version
```

## Quick start

### Backend

```bash
cd backend
python manage.py check --settings=config.settings.test
python manage.py makemigrations --check --dry-run --settings=config.settings.test
python -m ruff check apps config
python -m black --check apps config
python -m isort --profile black -o apps -o config --check-only apps config
python manage.py test --settings=config.settings.test
```
### Frontend

```bash
cd frontend
npm run typecheck
npm run build
```

## Documentation

Start with [`docs/README.en.md`](docs/README.en.md). It links to product documents, architecture, module descriptions, design system, development rules, and ADRs.

Useful entry points:

- [`docs/00-vision/product-vision.md`](docs/00-vision/product-vision.md)
- [`docs/01-architecture/project-structure.md`](docs/01-architecture/project-structure.md)
- [`docs/01-architecture/backend-architecture.md`](docs/01-architecture/backend-architecture.md)
- [`docs/01-architecture/frontend-architecture.md`](docs/01-architecture/frontend-architecture.md)
- [`docs/02-modules/users.md`](docs/02-modules/users.md)
- [`docs/02-modules/organizations.md`](docs/02-modules/organizations.md)
- [`docs/02-modules/calendar-and-notes.md`](docs/02-modules/calendar-and-notes.md)
- [`docs/02-modules/notifications.md`](docs/02-modules/notifications.md)
- [`docs/02-modules/feedback.md`](docs/02-modules/feedback.md)
- [`docs/02-modules/settings.md`](docs/02-modules/settings.md)

## Branches and commits

Commit conventions are documented in [`docs/04-development/commit-convention.md`](docs/04-development/commit-convention.md).

Examples:

```bash
git commit -m "feat(frontend): Add organization management page"
git commit -m "fix(backend): Fix notification delivery"
git commit -m "docs(project): Update root documentation"
```

## Security

Do not commit real secrets or user data:

- `.env`;
- tokens;
- passwords;
- SMTP keys;
- local databases;
- `.venv`;
- user files from `media/`.

Use only `.env.example` with safe placeholder values for examples.

## Status

The project is under active development. Documentation and README files should be updated together with functional modules, API changes, CI settings, and architecture updates.
---

<!-- DLE-Pifagor Root Footer -->
---

<p align="center">
  <sub>DLE "Pifagor" · unified digital learning environment</sub>
</p>

<p align="center">
  <a href="README.en.md">Project README</a> ·
  <a href="docs/README.en.md">Documentation</a> ·
  <a href="README.md">Русская версия</a>
</p>
<!-- /DLE-Pifagor Root Footer -->
