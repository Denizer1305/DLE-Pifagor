"""
Production-настройки проекта.

Используются на боевом сервере.

Важно:
    Все секреты должны приходить из переменных окружения.
"""

from config.api import get_bool_env, get_env, get_list_env
from config.settings.base import *  # noqa: F403

DEBUG = False

SECRET_KEY = get_env("DJANGO_SECRET_KEY", required=True)

ALLOWED_HOSTS = get_list_env(
    "DJANGO_ALLOWED_HOSTS",
    default=[],
)

if not ALLOWED_HOSTS:
    raise RuntimeError("DJANGO_ALLOWED_HOSTS must be set in production.")


DATABASES = {
    "default": {
        "ENGINE": get_env("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": get_env("DJANGO_DB_NAME", required=True),
        "USER": get_env("DJANGO_DB_USER", required=True),
        "PASSWORD": get_env("DJANGO_DB_PASSWORD", required=True),
        "HOST": get_env("DJANGO_DB_HOST", required=True),
        "PORT": get_env("DJANGO_DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------

SECURE_SSL_REDIRECT = get_bool_env("SECURE_SSL_REDIRECT", True)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool_env(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    True,
)
SECURE_HSTS_PRELOAD = get_bool_env("SECURE_HSTS_PRELOAD", True)

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

JWT_REFRESH_COOKIE_SECURE = True
JWT_REFRESH_COOKIE_SAMESITE = "Lax"


# -----------------------------------------------------------------------------
# CORS / CSRF
# -----------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = get_list_env("CORS_ALLOWED_ORIGINS", default=[])
CSRF_TRUSTED_ORIGINS = get_list_env("CSRF_TRUSTED_ORIGINS", default=[])


# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------

EMAIL_BACKEND = get_env(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = get_env("DJANGO_EMAIL_HOST", required=True)
EMAIL_PORT = int(get_env("DJANGO_EMAIL_PORT", 587))
EMAIL_HOST_USER = get_env("DJANGO_EMAIL_HOST_USER", required=True)
EMAIL_HOST_PASSWORD = get_env("DJANGO_EMAIL_HOST_PASSWORD", required=True)
EMAIL_USE_TLS = get_bool_env("DJANGO_EMAIL_USE_TLS", True)

DEFAULT_FROM_EMAIL = get_env("DJANGO_DEFAULT_FROM_EMAIL", required=True)
SERVER_EMAIL = DEFAULT_FROM_EMAIL


FRONTEND_BASE_URL = get_env(
    "FRONTEND_BASE_URL",
    "https://edu-pifagor.ru",
)

PIFAGOR_EMAIL_LOGO_URL = get_env(
    "PIFAGOR_EMAIL_LOGO_URL",
    "https://edu-pifagor.ru/static/emails/pifagor-logo-primary.png",
)

PIFAGOR_SUPPORT_EMAIL = get_env(
    "PIFAGOR_SUPPORT_EMAIL",
    "Pifagor-Platform33@yandex.ru",
)


# -----------------------------------------------------------------------------
# DRF renderers
# -----------------------------------------------------------------------------

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": get_env("DJANGO_LOG_LEVEL", "INFO"),
    },
}
