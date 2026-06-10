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

# Scripts

The `scripts` directory contains project utilities for local development, maintenance, and data preparation in DLE-Pifagor.

## Purpose

Scripts in this directory automate repeated operations:

- creating a superuser;
- generating `.env` or helper configuration files;
- exporting the API schema;
- resetting the local database;
- seeding demo data.

## Structure

- `create_superuser.sh` - superuser creation helper.
- `generate_env.py` - environment or configuration template generator.
- `export_schema.py` - API schema export helper.
- `reset_local_db.sh` - local database reset helper.
- `seed_demo_data.py` - demo data loader.

## Script rules

- A script name should clearly describe its action.
- Destructive operations should require explicit confirmation or be limited to local environments.
- If a script depends on backend or frontend context, mention it in the file comments.
- Python scripts that work with Django or the database should use the backend virtual environment.

## Running scripts

Before running a script, make sure the required environment is active and variables are configured. Backend operations usually require switching to `backend/` and using the project virtual environment.

Common commands should be documented next to the script or in the root `README.md` if most developers need them.
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
