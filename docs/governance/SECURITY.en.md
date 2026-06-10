<!-- DLE-Pifagor Root Header -->
<p align="center">
  <a href="README.en.md"><img src="design/logos/main/pifagor-logo-primary.svg" alt="DLE Pifagor" width="104" /></a>
</p>

<p align="center">
  <strong>DLE "Pifagor"</strong><br />
  <sub>Project root documentation · Security Policy</sub>
</p>

<p align="center">
  <a href="README.en.md">Project README</a> ·
  <a href="docs/README.en.md">Documentation</a> ·
  <a href="SECURITY.md">Русская версия</a>
</p>

---
<!-- /DLE-Pifagor Root Header -->

# Security Policy

## Reporting vulnerabilities

If you find a vulnerability in DLE "Pifagor", do not publish it in public issues. Send the details to the responsible maintainer or through the internal team channel.

Include:

- affected module;
- reproduction steps;
- expected and actual result;
- possible impact;
- logs or screenshots without secrets.

## Sensitive data

Do not commit:

- access or refresh tokens;
- passwords or secret keys;
- `.env` files with real values;
- personal user data;
- private keys, certificates, or backups;
- real DaData, email, Redis, PostgreSQL, or external service credentials.

## Access control

Keep permissions minimal. Administrative endpoints must validate both user role and active role. 401 and 403 errors should be handled explicitly and should not leak unnecessary details.

## Dependencies

Update dependencies carefully, checking changelogs and compatibility. Run backend and frontend checks after updates.

<!-- DLE-Pifagor Root Footer -->
---

<p align="center">
  <sub>DLE "Pifagor" · unified digital learning environment</sub>
</p>

<p align="center">
  <a href="README.en.md">Project README</a> ·
  <a href="docs/README.en.md">Documentation</a> ·
  <a href="SECURITY.md">Русская версия</a>
</p>
<!-- /DLE-Pifagor Root Footer -->
