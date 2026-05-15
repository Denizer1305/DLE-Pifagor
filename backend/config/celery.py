"""
Celery-конфигурация проекта.

Celery используется для фоновых задач:
    - отправка писем;
    - очистка временных данных;
    - отложенная анонимизация пользователей;
    - генерация отчётов;
    - будущие задачи ИИ-Анастасии.
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("pifagor")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Тестовая Celery-задача.

    Используется для быстрой проверки, что Celery корректно запускается.
    """

    print(f"Request: {self.request!r}")
