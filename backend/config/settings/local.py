"""
Локальные настройки проекта.

Используются для разработки на локальной машине.
"""

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

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


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
