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

# Infrastructure

The `infra` directory contains infrastructure files for DLE-Pifagor: Docker images, nginx configuration, deployment notes, and helper shell scripts.

## Structure

- `docker/` - Dockerfiles for platform services.
- `nginx/` - nginx configuration for local and production environments.
- `deploy/` - staging, production, and backup notes.
- `scripts/` - shell scripts used during startup and maintenance.

## Principles

- Infrastructure should be reproducible: a new developer or server should be able to follow documented steps.
- Production settings must not store secrets directly. Use environment variables and external `.env` files.
- Deployment scripts should be idempotent where possible.

## What belongs here

Only environment and delivery files belong in this directory: containers, reverse proxy configuration, backup scripts, entrypoints, wait-for scripts, and operational notes.

Application code, business logic, API, and UI components belong in `backend/` and `frontend/`.

## Related documents

- `../README.md` - project overview.
- `../backend/README.md` - backend development and checks.
- `../frontend/README.md` - frontend development and build.
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
