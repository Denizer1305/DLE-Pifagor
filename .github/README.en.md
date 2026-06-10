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

# GitHub configuration

This directory contains GitHub-specific configuration for the DLE-Pifagor repository: CI pipelines, quality gates, and automation support files.

## Structure

- `workflows/backend-ci.yml` - checks the backend: Django system checks, migrations, linting, formatting, and tests.
- `workflows/frontend-ci.yml` - checks the frontend: dependency installation, TypeScript, build, and static checks.

## Purpose

The files in this directory keep the project quality standard consistent before changes are merged. Backend and frontend checks are split so that failures remain easy to diagnose.

## When to update

Update `.github` files when:

- test or lint commands change;
- a new mandatory check is added;
- backend, frontend, or requirements structure changes;
- a new platform module needs its own CI step.

## Local checks

Before pushing, run the same commands used by the workflows. The main commands are documented in the root `README.md`, `backend/README.md`, and `frontend/README.md`.
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
