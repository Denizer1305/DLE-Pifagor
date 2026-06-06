# Pifagor — backend

Backend for the Pifagor educational platform built with Django and Django REST Framework. It powers authentication, users, dashboards, profile, settings, calendar, notes, notifications, feedback, and educational domain entities.

## Main Apps

- `users` — users, roles, profile, settings, and admin account management.
- `dashboard` — backend summaries for admin, teacher, student, and parent dashboards.
- `notifications` — notifications, delivery preferences, read state, and event generation.
- `feedback` — user requests, attachments, statuses, and admin notifications.
- `organizations` — educational organizations, structure, and organization codes.
- `education`, `courses`, `lessons`, `assignments`, `schedule` — educational platform domain.
- `achievements`, `portfolio`, `projects`, `olympiads`, `testing`, `journal`, `materials`, `analytics`, `ai` — additional domain areas.

## Structure

```text
apps/
  <module>/
    api|views/        HTTP endpoints and DRF viewsets
    serializers/     validation and API representation
    services/        business logic
    selectors/       read models and optimized queries
    models/          database models
    permissions/     access rules
    tests/           API and service tests
config/              Django settings and project configuration
fixtures/            seed data
media/               uploaded files in local development
static/              static assets
templates/           email and server-rendered templates
```

Large files should be split by responsibility. Serializer, view, and test files should stay under roughly 200 lines when the functionality naturally separates into smaller units.

## Setup

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements/dev.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

On Windows PowerShell, the virtualenv Python path usually looks like this:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

## Checks

```sh
DJANGO_SETTINGS_MODULE=config.settings.test .venv/bin/python manage.py check
DJANGO_SETTINGS_MODULE=config.settings.test .venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python -m ruff check apps config
.venv/bin/python -m black --check apps config
.venv/bin/python -m isort --profile black -o apps -o config --check-only apps config
```

For formatting:

```sh
.venv/bin/python -m black apps config
.venv/bin/python -m isort --profile black -o apps -o config apps config
```

## Implemented API Areas

- Authentication, refresh sessions, and frontend redirect on `401 Unauthorized`.
- User profile, backup email, phone, DaData city endpoints, and avatar upload.
- User settings: appearance, language, notifications, privacy, roles, and security.
- Dashboard summaries for admin, teacher, student, and parent roles.
- Calendar events and notes shown in dashboards and on calendar/notes pages.
- Notifications with preferences, counters, read state, and platform event integration.
- Feedback requests with attachments, statuses, email template, and notifications.
- Admin user list, user detail card, edit flow, and account lifecycle actions.

## Frontend Contracts

The frontend expects REST DTOs that are converted by mapper layers. When serializer fields change, update:

- `src/modules/<module>/types/*.types.ts`;
- `src/modules/<module>/mappers/*.mapper.ts`;
- the related service/composable;
- backend API tests.

For admin user creation, the frontend sends `POST /api/v1/users/admin/users/`. If the endpoint does not support creation yet, add a create serializer/service/viewset flow and return `AdminUserDetailSerializer`.

## Development Rules

- Views receive HTTP requests and delegate work to serializers/services.
- Serializers validate input and describe API representation.
- Selectors handle reads and optimized querysets.
- Services perform business operations and audit.
- Permissions enforce role-based access.
- Tests cover API contracts, permissions, and important service scenarios.
