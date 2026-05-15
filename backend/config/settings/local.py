"""
Локальные настройки проекта.

Используются для разработки на локальной машине.
"""

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

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

MIDDLEWARE = [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
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

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]