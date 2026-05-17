"""
Настройки тестового окружения.

Используются при запуске автоматических тестов.
"""

from config.settings.base import *  # noqa: F403

DEBUG = False

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# -----------------------------------------------------------------------------
# Frontend / Email branding for tests
# -----------------------------------------------------------------------------

FRONTEND_BASE_URL = "http://testserver"
PIFAGOR_EMAIL_LOGO_URL = "http://testserver/static/emails/pifagor-logo-primary.png"
PIFAGOR_SUPPORT_EMAIL = "support@example.com"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# -----------------------------------------------------------------------------
# Test database
# -----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

MIGRATION_MODULES = {
    # Если тесты станут медленными, сюда можно будет добавить приложения,
    # для которых временно отключаются миграции.
}


# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


# -----------------------------------------------------------------------------
# Cache
# -----------------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "pifagor-test-cache",
    }
}


# -----------------------------------------------------------------------------
# Cookies
# -----------------------------------------------------------------------------

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
JWT_REFRESH_COOKIE_SECURE = False


# -----------------------------------------------------------------------------
# DRF
# -----------------------------------------------------------------------------

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]
