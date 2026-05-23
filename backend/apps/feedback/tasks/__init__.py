"""
Фоновые задачи приложения feedback.

Сейчас уведомление администратору отправляется синхронно через service,
чтобы модуль работал без обязательного подключения Celery.

Позже сюда можно вынести:
    - send_feedback_admin_notification_task;
    - retry_failed_feedback_notifications_task;
    - cleanup_old_feedback_attachments_task.
"""

__all__: list[str] = []
