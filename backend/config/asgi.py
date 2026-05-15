"""
ASGI-конфигурация проекта.

Используется для запуска Django через ASGI-серверы.
В будущем сюда можно подключить WebSocket-слой через Django Channels.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_asgi_application()
