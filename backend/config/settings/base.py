"""
Базовые настройки Django-проекта.

Этот файл содержит настройки, общие для всех окружений:
local, production и test.

Здесь не должно быть секретов, которые нельзя хранить в репозитории.
Секреты и значения, зависящие от окружения, читаются из переменных окружения.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from config.api import get_bool_env, get_env, get_int_env, get_list_env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = get_env(
    "DJANGO_SECRET_KEY",
    "unsafe-local-development-secret-key",
)

DEBUG = get_bool_env("DJANGO_DEBUG", False)

ALLOWED_HOSTS = get_list_env(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"],
)


# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "django_celery_beat",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.organizations.apps.OrganizationsConfig",
    "apps.users.apps.UsersConfig",
    "apps.feedback.apps.FeedbackConfig",
    "apps.dashboard.apps.DashboardConfig",
    "apps.notifications.apps.NotificationsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -----------------------------------------------------------------------------
# URL / WSGI / ASGI
# -----------------------------------------------------------------------------

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": get_env("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": get_env("DJANGO_DB_NAME", "pifagor"),
        "USER": get_env("DJANGO_DB_USER", "pifagor"),
        "PASSWORD": get_env("DJANGO_DB_PASSWORD", "pifagor"),
        "HOST": get_env("DJANGO_DB_HOST", "localhost"),
        "PORT": get_env("DJANGO_DB_PORT", "5432"),
        "CONN_MAX_AGE": get_int_env("DJANGO_DB_CONN_MAX_AGE", 60),
    }
}


# -----------------------------------------------------------------------------
# Custom User
# -----------------------------------------------------------------------------

AUTH_USER_MODEL = "users.User"


# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": get_int_env("DJANGO_PASSWORD_MIN_LENGTH", 8),
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------

LANGUAGE_CODE = get_env("DJANGO_LANGUAGE_CODE", "ru-ru")
TIME_ZONE = get_env("DJANGO_TIME_ZONE", "Europe/Moscow")

USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Static / Media
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (
    [
        BASE_DIR / "static",
    ]
    if (BASE_DIR / "static").exists()
    else []
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# -----------------------------------------------------------------------------
# Default primary key
# -----------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -----------------------------------------------------------------------------
# Django REST Framework
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "apps.core.permissions.IsAuthenticatedAndActive",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.DefaultPageNumberPagination",
    "PAGE_SIZE": get_int_env("DRF_PAGE_SIZE", 20),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.core.exceptions_handler.custom_exception_handler",
    "DEFAULT_THROTTLE_RATES": {
        "contact_feedback": "3/10min",
    },
}


# -----------------------------------------------------------------------------
# OpenAPI / Swagger
# -----------------------------------------------------------------------------

SPECTACULAR_SETTINGS = {
    "TITLE": "ЦОС «Пифагор» API",
    "DESCRIPTION": "API цифровой образовательной среды «Пифагор».",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}


# -----------------------------------------------------------------------------
# Simple JWT
# -----------------------------------------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=get_int_env("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", 10)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=get_int_env("JWT_REFRESH_TOKEN_LIFETIME_DAYS", 7)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": get_env("JWT_SIGNING_KEY", SECRET_KEY),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


# -----------------------------------------------------------------------------
# JWT cookies
# -----------------------------------------------------------------------------

JWT_REFRESH_COOKIE_NAME = get_env("JWT_REFRESH_COOKIE_NAME", "pifagor_refresh")
JWT_REFRESH_COOKIE_PATH = get_env("JWT_REFRESH_COOKIE_PATH", "/api/v1/users/auth/")
JWT_REFRESH_COOKIE_SECURE = get_bool_env("JWT_REFRESH_COOKIE_SECURE", False)
JWT_REFRESH_COOKIE_HTTP_ONLY = True
JWT_REFRESH_COOKIE_SAMESITE = get_env("JWT_REFRESH_COOKIE_SAMESITE", "Lax")


# -----------------------------------------------------------------------------
# CORS / CSRF
# -----------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = get_list_env(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = get_list_env(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
)


# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

EMAIL_BACKEND = get_env(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = get_env("DJANGO_EMAIL_HOST", "")
EMAIL_PORT = get_int_env("DJANGO_EMAIL_PORT", 25)
EMAIL_HOST_USER = get_env("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = get_env("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = get_bool_env("DJANGO_EMAIL_USE_TLS", False)
EMAIL_USE_SSL = get_bool_env("DJANGO_EMAIL_USE_SSL", False)
EMAIL_TIMEOUT = get_int_env("DJANGO_EMAIL_TIMEOUT", 20)

DEFAULT_FROM_EMAIL = get_env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    "noreply@pifagor.local",
)

SERVER_EMAIL = DEFAULT_FROM_EMAIL


# -----------------------------------------------------------------------------
# Frontend / Email branding
# -----------------------------------------------------------------------------

FRONTEND_BASE_URL = get_env(
    "FRONTEND_BASE_URL",
    "http://localhost:5173",
)

EMAIL_VERIFY_PATH = get_env(
    "EMAIL_VERIFY_PATH",
    "/auth/verify-email",
)

PASSWORD_RESET_PATH = get_env(
    "PASSWORD_RESET_PATH",
    "/auth/reset-password",
)

EMAIL_LOGO_URL = get_env(
    "EMAIL_LOGO_URL",
    "",
)

DADATA_API_TOKEN = get_env("DADATA_API_TOKEN", "")
DADATA_SUGGESTIONS_URL = get_env(
    "DADATA_SUGGESTIONS_URL",
    "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
)


# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------

CELERY_BROKER_URL = get_env("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = get_env("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = get_int_env("CELERY_TASK_TIME_LIMIT", 30 * 60)
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 5
CELERY_ACCEPT_CONTENT = [
    "json",
]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULE = {
    "users-deactivate-expired-invite-codes-every-30-minutes": {
        "task": "apps.users.tasks.cleanup_tasks.deactivate_expired_invite_codes_task",
        "schedule": crontab(minute="*/30"),
    },
    "users-expire-old-join-requests-hourly": {
        "task": "apps.users.tasks.cleanup_tasks.expire_old_join_requests_task",
        "schedule": crontab(minute=0),
    },
    "users-anonymize-scheduled-users-hourly": {
        "task": "apps.users.tasks.lifecycle_tasks.anonymize_scheduled_users_task",
        "schedule": crontab(minute=10),
    },
    "users-cleanup-unused-expired-invite-codes-daily": {
        "task": "apps.users.tasks.cleanup_tasks.cleanup_unused_expired_invite_codes_task",
        "schedule": crontab(hour=3, minute=30),
        "kwargs": {
            "days": 30,
        },
    },
}

CELERY_IMPORTS = (
    "apps.users.tasks.cleanup_tasks",
    "apps.users.tasks.lifecycle_tasks",
    "apps.users.tasks.emails.registration_email_tasks",
    "apps.users.tasks.emails.join_request_email_tasks",
    "apps.users.tasks.emails.guardian_email_tasks",
    "apps.users.tasks.emails.lifecycle_email_tasks",
)

# -----------------------------------------------------------------------------
# Security basics
# -----------------------------------------------------------------------------

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False

SESSION_COOKIE_SECURE = get_bool_env("SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = get_bool_env("CSRF_COOKIE_SECURE", not DEBUG)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# -----------------------------------------------------------------------------
# Project settings
# -----------------------------------------------------------------------------

PIFAGOR_PROJECT_NAME = "ЦОС «Пифагор»"
PIFAGOR_API_PREFIX = "/api/v1"
PIFAGOR_ACCOUNT_DELETION_GRACE_DAYS = get_int_env(
    "PIFAGOR_ACCOUNT_DELETION_GRACE_DAYS",
    7,
)
