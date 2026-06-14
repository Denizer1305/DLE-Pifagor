<!-- DLE-Pifagor Documentation Header -->
<p align="center">
  <a href="../../README.md"><img src="../../design/logos/main/pifagor-logo-primary.svg" alt="DLE-Pifagor" width="96" /></a>
</p>

<p align="center">
  <a href="../../docs/README.md">Документация</a> ·
  <a href="../../docs/README.en.md">English version</a> ·
  <a href="../../README.md">README проекта</a>
</p>

---
<!-- /DLE-Pifagor Documentation Header -->
# Локальный запуск

## Требования

- Node.js `20.19+` или `22.12+`;
- Python `3.12+`;
- PostgreSQL для окружений, где не используется SQLite;
- Redis для фоновых задач;
- Git;
- `make`, если используется корневой `Makefile`.

## Быстрый запуск через Makefile

Из корня репозитория:

```sh
make env-copy
make backend-install
make frontend-install
make backend-run
make frontend-run
```

Полезные проверки:

```sh
make backend-ci
make frontend-ci
make check
```

`make ci` сейчас запускает backend CI. Полная локальная проверка с pre-commit
описана целью `make check`.

## Backend вручную

Команды запускаются из папки `backend`.

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements/local.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/local.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

## Frontend вручную

Команды запускаются из папки `frontend`.

```sh
npm install
npm run dev
```

Проверки:

```sh
npm run typecheck
npm run build
```

В `package.json` также есть alias `npm run type-check`.

## OpenAPI

Snapshot схемы можно обновить из папки `backend`:

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.test"
..\.venv\Scripts\python.exe manage.py spectacular --file ..\docs\06-api\openapi.yaml
```

Документация доступна на backend:

- `/api/schema/`;
- `/api/docs/`;
- `/api/redoc/`.

## Celery и Redis

Redis должен быть запущен до старта фоновых задач. Celery используется для
email, уведомлений и фоновой обработки, если соответствующие задачи включены в
окружении.

## Первичная проверка

После запуска проверьте:

- публичные страницы открываются;
- вход и refresh token работают;
- личные кабинеты доступны согласно роли;
- API отвечает на `/api/schema/`;
- Swagger UI открывается на `/api/docs/`;
- ReDoc открывается на `/api/redoc/`.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
