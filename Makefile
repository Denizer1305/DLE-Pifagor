# ==============================================================================
# DLE-Pifagor Makefile
# ==============================================================================

SHELL := /bin/bash

PROJECT_NAME := DLE-Pifagor

BACKEND_DIR := backend
FRONTEND_DIR := frontend

ifeq ($(OS),Windows_NT)
VENV_BIN ?= .venv/Scripts
PYTHON ?= $(VENV_BIN)/python.exe
PIP ?= $(VENV_BIN)/pip.exe
else
VENV_BIN ?= .venv/bin
PYTHON ?= $(VENV_BIN)/python
PIP ?= $(VENV_BIN)/pip
endif

MANAGE := $(PYTHON) manage.py
CI_DJANGO_SETTINGS := DJANGO_SETTINGS_MODULE=config.settings.test

BACKEND_REQUIREMENTS_LOCAL := requirements/local.txt
BACKEND_REQUIREMENTS_TEST := requirements/test.txt
BACKEND_REQUIREMENTS_PRODUCTION := requirements/production.txt

.DEFAULT_GOAL := help


# ==============================================================================
# Help
# ==============================================================================

.PHONY: help
help: ## Показать список доступных команд
	@echo ""
	@echo "$(PROJECT_NAME)"
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-28s %s\n", $$1, $$2}'
	@echo ""


# ==============================================================================
# Environment
# ==============================================================================

.PHONY: env-copy
env-copy: ## Создать .env из .env.example, если .env ещё нет
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created from .env.example"; \
	else \
		echo ".env already exists"; \
	fi


# ==============================================================================
# Backend: install
# ==============================================================================

.PHONY: backend-install
backend-install: ## Установить backend-зависимости для локальной разработки
	cd $(BACKEND_DIR) && $(PIP) install -r $(BACKEND_REQUIREMENTS_LOCAL)

.PHONY: backend-install-test
backend-install-test: ## Установить backend-зависимости для тестов
	cd $(BACKEND_DIR) && $(PIP) install -r $(BACKEND_REQUIREMENTS_TEST)

.PHONY: backend-install-production
backend-install-production: ## Установить backend-зависимости для production
	cd $(BACKEND_DIR) && $(PIP) install -r $(BACKEND_REQUIREMENTS_PRODUCTION)


# ==============================================================================
# Backend: Django
# ==============================================================================

.PHONY: backend-check
backend-check: ## Проверить Django-проект
	cd $(BACKEND_DIR) && $(CI_DJANGO_SETTINGS) $(MANAGE) check

.PHONY: backend-makemigrations
backend-makemigrations: ## Создать миграции backend
	cd $(BACKEND_DIR) && $(MANAGE) makemigrations

.PHONY: backend-check-migrations
backend-check-migrations: ## Проверить, что миграции не забыты
	cd $(BACKEND_DIR) && $(CI_DJANGO_SETTINGS) $(MANAGE) makemigrations --check --dry-run

.PHONY: backend-migrate
backend-migrate: ## Применить миграции backend
	cd $(BACKEND_DIR) && $(MANAGE) migrate

.PHONY: backend-superuser
backend-superuser: ## Создать суперпользователя Django
	cd $(BACKEND_DIR) && $(MANAGE) createsuperuser

.PHONY: backend-shell
backend-shell: ## Открыть Django shell
	cd $(BACKEND_DIR) && $(MANAGE) shell

.PHONY: backend-run
backend-run: ## Запустить backend dev server
	cd $(BACKEND_DIR) && $(MANAGE) runserver 0.0.0.0:8000

.PHONY: backend-collectstatic
backend-collectstatic: ## Собрать static-файлы
	cd $(BACKEND_DIR) && $(MANAGE) collectstatic --noinput


# ==============================================================================
# Backend: quality
# ==============================================================================

.PHONY: backend-lint
backend-lint: ## Проверить backend через ruff
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff check apps config

.PHONY: backend-format
backend-format: ## Отформатировать backend через ruff, black и isort
	cd $(BACKEND_DIR) && $(PYTHON) -m ruff check apps config --fix
	cd $(BACKEND_DIR) && $(PYTHON) -m black apps config
	cd $(BACKEND_DIR) && $(PYTHON) -m isort --profile black -o apps -o config apps config

.PHONY: backend-format-check
backend-format-check: ## Проверить форматирование backend
	cd $(BACKEND_DIR) && $(PYTHON) -m black --check apps config
	cd $(BACKEND_DIR) && $(PYTHON) -m isort --profile black -o apps -o config --check-only apps config

.PHONY: backend-test
backend-test: ## Запустить backend-тесты
	cd $(BACKEND_DIR) && $(CI_DJANGO_SETTINGS) $(PYTHON) -m pytest

.PHONY: backend-test-cov
backend-test-cov: ## Запустить backend-тесты с coverage
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest --cov=apps --cov-report=term-missing --cov-report=html

.PHONY: backend-ci
backend-ci: backend-check backend-check-migrations backend-lint backend-format-check backend-test ## Локально выполнить backend CI


# ==============================================================================
# Frontend
# ==============================================================================

.PHONY: frontend-install
frontend-install: ## Установить frontend-зависимости
	cd $(FRONTEND_DIR) && npm install

.PHONY: frontend-ci-install
frontend-ci-install: ## Установить frontend-зависимости через npm ci
	cd $(FRONTEND_DIR) && npm ci

.PHONY: frontend-run
frontend-run: ## Запустить frontend dev server
	cd $(FRONTEND_DIR) && npm run dev

.PHONY: frontend-build
frontend-build: ## Собрать frontend
	cd $(FRONTEND_DIR) && npm run build

.PHONY: frontend-preview
frontend-preview: ## Запустить preview frontend-сборки
	cd $(FRONTEND_DIR) && npm run preview

.PHONY: frontend-lint
frontend-lint: ## Запустить frontend lint, если script существует
	cd $(FRONTEND_DIR) && npm run lint --if-present

.PHONY: frontend-typecheck
frontend-typecheck: ## Запустить frontend typecheck, если script существует
	cd $(FRONTEND_DIR) && npm run typecheck --if-present

.PHONY: frontend-test
frontend-test: ## Запустить frontend unit tests, если script существует
	cd $(FRONTEND_DIR) && npm run test:unit --if-present

.PHONY: frontend-ci
frontend-ci: frontend-ci-install frontend-lint frontend-typecheck frontend-test frontend-build ## Локально выполнить frontend CI


# ==============================================================================
# Docker
# ==============================================================================

.PHONY: docker-build
docker-build: ## Собрать Docker-контейнеры
	docker compose build

.PHONY: docker-up
docker-up: ## Запустить проект через docker compose
	docker compose up -d

.PHONY: docker-down
docker-down: ## Остановить docker compose
	docker compose down

.PHONY: docker-logs
docker-logs: ## Показать логи docker compose
	docker compose logs -f

.PHONY: docker-restart
docker-restart: docker-down docker-up ## Перезапустить docker compose


# ==============================================================================
# Database / local utilities
# ==============================================================================

.PHONY: reset-local-db
reset-local-db: ## Сбросить локальную SQLite-БД и миграции применить заново
	rm -f $(BACKEND_DIR)/db.sqlite3
	cd $(BACKEND_DIR) && $(MANAGE) migrate

.PHONY: seed-demo-data
seed-demo-data: ## Запустить скрипт демо-данных
	$(PYTHON) scripts/seed_demo_data.py


# ==============================================================================
# Full project checks
# ==============================================================================

.PHONY: install
install: backend-install frontend-install ## Установить backend и frontend зависимости

.PHONY: ci
ci: backend-ci ## Выполнить backend CI-проверки

.PHONY: run
run: ## Подсказка по запуску backend и frontend
	@echo "Run backend:"
	@echo "  make backend-run"
	@echo ""
	@echo "Run frontend:"
	@echo "  make frontend-run"
	@echo ""
	@echo "Or use Docker:"
	@echo "  make docker-up"

# ==============================================================================
# Pre-commit
# ==============================================================================

.PHONY: precommit-install
precommit-install: ## Установить pre-commit hooks
	pre-commit install
	pre-commit install --hook-type pre-push

.PHONY: precommit-run
precommit-run: ## Запустить pre-commit на всех файлах
	pre-commit run --all-files

.PHONY: precommit-update
precommit-update: ## Обновить версии pre-commit hooks
	pre-commit autoupdate

.PHONY: precommit-clean
precommit-clean: ## Очистить cache pre-commit
	pre-commit clean


.PHONY: install
install: backend-install frontend-install precommit-install ## Установить зависимости и pre-commit hooks

.PHONY: check
check: precommit-run ci ## Выполнить pre-commit и полный локальный CI
