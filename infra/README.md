<!-- DLE-Pifagor README Header -->
<p align="center">
  <a href="../README.md"><img src="../design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Документация проекта и материалы разработки</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor README Header -->

# Infrastructure

Папка `infra` предназначена для инфраструктурных файлов платформы DLE-Pifagor: Docker-образов, nginx-конфигураций, сценариев деплоя и вспомогательных shell-скриптов.

## Структура

- `docker/` - Dockerfile-файлы для сервисов платформы.
- `nginx/` - конфигурации nginx для локального и production-окружения.
- `deploy/` - заметки и инструкции по staging, production и backup-сценариям.
- `scripts/` - shell-скрипты, которые используются при запуске и обслуживании окружения.

## Принципы

- Инфраструктура должна быть воспроизводимой: новый разработчик или сервер должны подниматься по описанным шагам.
- Production-настройки не должны хранить секреты напрямую. Используйте переменные окружения и `.env`-файлы вне репозитория.
- Скрипты деплоя должны быть идемпотентными там, где это возможно.

## Что хранить здесь

В эту папку попадают только файлы, связанные с окружением и доставкой приложения: контейнеры, reverse proxy, backup, entrypoint, wait-for scripts и инструкции эксплуатации.

Код приложения, бизнес-логика, API и UI-компоненты должны оставаться в `backend/` и `frontend/`.

## Связанные документы

- `../README.md` - общее описание проекта.
- `../backend/README.md` - backend-разработка и проверки.
- `../frontend/README.md` - frontend-разработка и сборка.
---

<!-- DLE-Pifagor README Footer -->
---

<p align="center">
  <sub>ЦОС "Пифагор" · единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>
<!-- /DLE-Pifagor README Footer -->
