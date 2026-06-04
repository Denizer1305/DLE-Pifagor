from __future__ import annotations

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("pifagor")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.conf.beat_schedule = {
    "notifications-generate-daily": {
        "task": "notifications.generate_daily_notifications",
        "schedule": crontab(hour=7, minute=0),
    },
    "notifications-generate-overdue": {
        "task": "notifications.generate_overdue_notifications",
        "schedule": crontab(hour=0, minute=1),
    },
    "notifications-generate-note-reminders": {
        "task": "notifications.generate_note_reminder_notifications",
        "schedule": crontab(minute="*/15"),
    },
    "notifications-cleanup-expired": {
        "task": "notifications.cleanup_expired_notifications",
        "schedule": crontab(hour=3, minute=30),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Тестовая задача Celery.

    Используется для быстрой проверки, что Celery worker
    корректно видит проект Django и может выполнять задачи.
    """

    print(f"Request: {self.request!r}")
