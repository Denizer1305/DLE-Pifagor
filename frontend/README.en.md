# Pifagor — frontend

Frontend for the Pifagor educational platform built with Vue 3, TypeScript, and Vite. The app includes public pages, authentication, role dashboards, profile management, settings, notifications, calendar, notes, feedback, and admin tools.

## Stack

- Vue 3 + Composition API
- TypeScript
- Vite
- Vue Router
- Pinia
- Axios
- Font Awesome

## Main Modules

- `auth` — login, registration, email verification, password reset, and logout page.
- `public` — home, about, teachers, contacts, and public feedback form.
- `admin` — admin dashboard, users, user create/edit/detail pages, feedback, calendar, and notes.
- `teacher` — teacher dashboard powered by backend data.
- `student` — student dashboard with learning workspace and empty-data states.
- `parent` — parent dashboard based on the shared dashboard layout.
- `profile` — user profile, edit flow, avatar upload/crop, DaData city suggestions, and phone mask.
- `settings` — appearance, themes, language, notifications, privacy, roles, and security.
- `calendar` — full calendar page, event creation, and day plan.
- `notes` — personal notes, calendar integration, and notes page.
- `notifications` — notification feed, dropdown, counters, read state, and notification settings.
- `feedback` — user requests with attachments, statuses, and notification integration.

## Architecture

Modules follow the same structure:

- `api` — low-level HTTP requests.
- `services` — backend-oriented use cases.
- `mappers` — DTO to UI model conversion.
- `types` — DTOs, UI models, and payload types.
- `data` — copy, options, and static configuration.
- `composables` — state and user flows.
- `components` — dumb presentational components.
- `pages` — thin pages that compose shell, composables, and components.

Shared dashboard components live in `src/components/dashboard`. Reuse them for cards, shell, topbar, sidebar, calendar panels, notifications, and notes.

## Setup

```sh
npm install
npm run dev
```

The frontend expects the project backend API in the local environment. The API base URL is configured through the HTTP client and project env settings.

## Checks

```sh
npm run type-check
npm run build
```

`npm run build` runs TypeScript checks and the production build.

## Backend Integration

The frontend uses REST API for:

- authentication and refresh sessions;
- admin, teacher, student, and parent dashboard summaries;
- profile and user settings;
- calendar events and notes;
- notifications and notification settings;
- feedback requests and attachments;
- admin user management.

If a new UI flow sends a payload and the backend returns `400`, `401`, `403`, `404`, or `405`, check the matching backend serializer, view, and service first.

## Themes and Localization

Light, dark, and system display modes are supported. The color theme controls CSS variables and the logo from `src/assets/brand/logo/themes`.

The interface language is selected in appearance settings. UI copy should live in `*.data.ts` or i18n dictionaries, not inside components.

## Development Rules

- Keep pages thin.
- Keep components presentational and prop-driven.
- Store copy in `data` or translations.
- Move logic to composables/services.
- Convert DTOs in mappers.
- Use shared `BaseSelect` for selects.
- Reuse shared dashboard cards before creating new ones.
