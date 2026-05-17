from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.users.constants.audit import AuditActorType, UserAuditAction
from apps.users.constants.onboarding import RegistrationAttemptStatus
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserAuditLog(TimeStampedModel):
    """
    Журнал аудита действий пользователя.

    Хранит важные события:
        - регистрация;
        - подтверждение email;
        - назначение роли;
        - создание заявки;
        - подтверждение заявки;
        - отклонение заявки;
        - блокировка;
        - архивация;
        - анонимизация.

    Аудит нужен, чтобы не потеряться в действиях системы.
    """

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="performed_user_audit_logs",
        verbose_name=_("Инициатор"),
        blank=True,
        null=True,
    )
    actor_type = models.CharField(
        _("Тип инициатора"),
        max_length=32,
        choices=AuditActorType.choices,
        default=AuditActorType.USER,
    )

    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_audit_logs",
        verbose_name=_("Целевой пользователь"),
        blank=True,
        null=True,
    )

    action = models.CharField(
        _("Действие"),
        max_length=64,
        choices=UserAuditAction.choices,
        db_index=True,
    )

    message = models.TextField(
        _("Сообщение"),
        blank=True,
    )
    metadata = models.JSONField(
        _("Метаданные"),
        default=dict,
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

    class Meta:
        db_table = "users_audit_log"
        verbose_name = _("Запись аудита пользователя")
        verbose_name_plural = _("Аудит пользователей")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["action"], name="users_audit_action_idx"),
            models.Index(fields=["target_user"], name="users_audit_target_idx"),
            models.Index(fields=["created_at"], name="users_audit_created_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление записи аудита.

        Returns:
            str: Действие аудита.
        """

        return f"{self.get_action_display()} — {self.target_user or 'без пользователя'}"


class RegistrationAttemptLog(TimeStampedModel):
    """
    Журнал попыток регистрации.

    Используется для:
        - фиксации неудачных попыток ввода кода организации;
        - ограничения количества запросов;
        - защиты от подбора кодов.

    Важно:
        Если код организации неверный, пользователь и заявка не создаются,
        но попытка может быть записана сюда без лишних персональных данных.
    """

    email_hash = models.CharField(
        _("Хеш email"),
        max_length=128,
        db_index=True,
        blank=True,
    )
    phone_hash = models.CharField(
        _("Хеш телефона"),
        max_length=128,
        db_index=True,
        blank=True,
    )

    role_code = models.CharField(
        _("Код роли"),
        max_length=64,
        blank=True,
        db_index=True,
    )
    status = models.CharField(
        _("Статус попытки"),
        max_length=32,
        choices=RegistrationAttemptStatus.choices,
        default=RegistrationAttemptStatus.FAILED,
        db_index=True,
    )

    failure_reason = models.CharField(
        _("Причина ошибки"),
        max_length=255,
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

    metadata = models.JSONField(
        _("Метаданные"),
        default=dict,
        blank=True,
    )

    class Meta:
        db_table = "users_registration_attempt_log"
        verbose_name = _("Попытка регистрации")
        verbose_name_plural = _("Попытки регистрации")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["email_hash"], name="users_reg_email_hash_idx"),
            models.Index(fields=["phone_hash"], name="users_reg_phone_hash_idx"),
            models.Index(fields=["ip_address"], name="users_reg_ip_idx"),
            models.Index(fields=["status"], name="users_reg_status_idx"),
            models.Index(fields=["created_at"], name="users_reg_created_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление попытки регистрации.

        Returns:
            str: Статус и роль.
        """

        return f"{self.get_status_display()} — {self.role_code or 'роль не указана'}"
