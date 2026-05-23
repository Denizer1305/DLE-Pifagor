from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("pifagor")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Тестовая задача Celery.

    Используется для быстрой проверки, что Celery worker
    корректно видит проект Django и может выполнять задачи.
    """

    print(f"Request: {self.request!r}")
