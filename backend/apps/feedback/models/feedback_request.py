from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class FeedbackRequest(TimeStampedModel):
    class TopicChoices(models.TextChoices):
        QUESTION = "question", _("Вопрос")
        PARTNERSHIP = "partnership", _("Сотрудничество")
        ORGANIZATION_CONNECTION = "organization_connection", _(
            "Подключение организации"
        )
        TECHNICAL_SUPPORT = "technical_support", _("Техническая поддержка")
        BUG = "bug", _("Ошибка")
        OTHER = "other", _("Другое")

    class SourceChoices(models.TextChoices):
        CONTACTS_PAGE = "contacts_page", _("Страница контактов")
        ERROR_MODAL = "error_modal", _("Модальное окно ошибки")
        SYSTEM = "system", _("Система")

    class StatusChoices(models.TextChoices):
        NEW = "new", _("Новое")
        IN_PROGRESS = "in_progress", _("В работе")
        ANSWERED = "answered", _("Ответ отправлен")
        CLOSED = "closed", _("Закрыто")
        SPAM = "spam", _("Спам")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="feedback_requests",
        verbose_name=_("Пользователь"),
        blank=True,
        null=True,
    )
    topic = models.CharField(
        _("Тема обращения"),
        max_length=64,
        choices=TopicChoices.choices,
        default=TopicChoices.QUESTION,
        db_index=True,
    )
    source = models.CharField(
        _("Источник"),
        max_length=64,
        choices=SourceChoices.choices,
        default=SourceChoices.CONTACTS_PAGE,
        db_index=True,
    )
    status = models.CharField(
        _("Статус"),
        max_length=64,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
        db_index=True,
    )

    full_name = models.CharField(
        _("Имя"),
        max_length=255,
    )
    email = models.EmailField(
        _("Email"),
    )
    phone = models.CharField(
        _("Телефон"),
        max_length=32,
        blank=True,
    )
    organization_name = models.CharField(
        _("Организация"),
        max_length=255,
        blank=True,
    )

    subject = models.CharField(
        _("Тема письма"),
        max_length=255,
        blank=True,
    )
    message = models.TextField(
        _("Сообщение"),
    )
    is_personal_data_consent = models.BooleanField(
        _("Согласие на обработку персональных данных"),
        default=False,
    )

    page_url = models.URLField(
        _("URL страницы"),
        blank=True,
    )
    frontend_route = models.CharField(
        _("Frontend route"),
        max_length=255,
        blank=True,
    )
    error_code = models.CharField(
        _("Код ошибки"),
        max_length=120,
        blank=True,
    )
    error_details = models.TextField(
        _("Технические детали ошибки"),
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        _("IP-адрес"),
        blank=True,
        null=True,
    )
    user_agent = models.TextField(
        _("User-Agent"),
        blank=True,
    )

    admin_notification_sent = models.BooleanField(
        _("Уведомление администратору отправлено"),
        default=False,
    )
    admin_notification_error = models.TextField(
        _("Ошибка отправки уведомления"),
        blank=True,
    )

    class Meta:
        db_table = "feedback_request"
        verbose_name = _("Обращение")
        verbose_name_plural = _("Обращения")
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=["status", "created_at"],
                name="fb_req_status_idx",
            ),
            models.Index(
                fields=["topic", "created_at"],
                name="fb_req_topic_idx",
            ),
            models.Index(
                fields=["source", "created_at"],
                name="fb_req_source_idx",
            ),
            models.Index(
                fields=["email", "created_at"],
                name="fb_req_email_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} — {self.get_topic_display()}"
