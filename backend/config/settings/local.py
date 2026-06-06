"""
Локальные настройки проекта.

Используются для разработки на локальной машине.
"""

from config.api import get_bool_env, get_env, get_int_env
from config.settings.base import INSTALLED_APPS as BASE_INSTALLED_APPS
from config.settings.base import MIDDLEWARE as BASE_MIDDLEWARE
from config.settings.base import REST_FRAMEWORK as BASE_REST_FRAMEWORK
from config.settings.base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]


# -----------------------------------------------------------------------------
# Debug Toolbar
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    *BASE_INSTALLED_APPS,
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *BASE_MIDDLEWARE,
]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]


# -----------------------------------------------------------------------------
# Local CORS / CSRF
# -----------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


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
# Frontend / Email branding for local development
# -----------------------------------------------------------------------------

FRONTEND_BASE_URL = "http://localhost:5173"
EMAIL_LOGO_URL = "http://localhost:5173/email/logo-pifagor.png"
SUPPORT_EMAIL = "Pifagor-Platform33@yandex.ru"
PIFAGOR_EMAIL_LOGO_URL = EMAIL_LOGO_URL
PIFAGOR_SUPPORT_EMAIL = SUPPORT_EMAIL


# -----------------------------------------------------------------------------
# Cookies
# -----------------------------------------------------------------------------

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
JWT_REFRESH_COOKIE_SECURE = False


# -----------------------------------------------------------------------------
# DRF Browsable API
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    **BASE_REST_FRAMEWORK,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# Celery в локальной разработке выполняет задачи сразу, без Redis.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# В eager-режиме результат задач не нужен.
CELERY_TASK_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = None
