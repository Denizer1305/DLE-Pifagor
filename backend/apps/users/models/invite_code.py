from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.core.utils import generate_random_code, hash_value
from apps.users.constants.onboarding import InviteCodePurpose
from apps.users.managers import InviteCodeManager
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class InviteCode(TimeStampedModel):
    """
    Временный код приглашения.

    Используется для:
        - регистрации преподавателя в организации;
        - подтверждения связи родителя с учащимся;
        - передачи части кода от куратора;
        - передачи части кода от учащегося старше 14 лет.

    Важно:
        Сам код не хранится в открытом виде.
        В базе хранится только code_hash.
    """

    objects = InviteCodeManager()

    code_hash = models.CharField(
        _("Хеш кода"),
        max_length=128,
        unique=True,
        db_index=True,
    )

    purpose = models.CharField(
        _("Назначение кода"),
        max_length=64,
        choices=InviteCodePurpose.choices,
        db_index=True,
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="invite_codes",
        verbose_name=_("Образовательная организация"),
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="invite_codes",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.SET_NULL,
        related_name="invite_codes",
        verbose_name=_("Группа"),
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_invite_codes",
        verbose_name=_("Создал"),
        blank=True,
        null=True,
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="targeted_invite_codes",
        verbose_name=_("Целевой пользователь"),
        blank=True,
        null=True,
    )

    expires_at = models.DateTimeField(
        _("Дата истечения"),
    )
    max_uses = models.PositiveIntegerField(
        _("Максимальное количество использований"),
        default=1,
    )
    used_count = models.PositiveIntegerField(
        _("Количество использований"),
        default=0,
    )

    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )
    last_used_at = models.DateTimeField(
        _("Дата последнего использования"),
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "users_invite_code"
        verbose_name = _("Код приглашения")
        verbose_name_plural = _("Коды приглашения")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["code_hash"], name="users_invite_hash_idx"),
            models.Index(
                fields=["purpose", "is_active"], name="users_invite_purpose_idx"
            ),
            models.Index(fields=["organization"], name="users_invite_org_idx"),
            models.Index(fields=["expires_at"], name="users_invite_expires_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление кода.

        Returns:
            str: Назначение кода и организация.
        """

        return (
            f"{self.get_purpose_display()} — {self.organization or 'без организации'}"
        )

    @staticmethod
    def make_code(length: int = 10) -> str:
        """
        Генерирует новый человекочитаемый код.

        Args:
            length:
                Длина кода.

        Returns:
            str: Сгенерированный код.
        """

        return generate_random_code(length=length)

    @staticmethod
    def make_hash(code: str) -> str:
        """
        Создаёт хеш кода приглашения.

        Args:
            code:
                Исходный код.

        Returns:
            str: Хеш кода.
        """

        return hash_value(code)

    @property
    def is_expired(self) -> bool:
        """
        Проверяет, истёк ли срок действия кода.

        Returns:
            bool: True, если код истёк.
        """

        return timezone.now() >= self.expires_at

    @property
    def is_usage_limit_reached(self) -> bool:
        """
        Проверяет, достигнут ли лимит использований.

        Returns:
            bool: True, если лимит использований достигнут.
        """

        return self.used_count >= self.max_uses

    @property
    def is_available(self) -> bool:
        """
        Проверяет, можно ли использовать код.

        Returns:
            bool: True, если код активен, не истёк и не исчерпал лимит.
        """

        return (
            self.is_active and not self.is_expired and not self.is_usage_limit_reached
        )

    def mark_used(self, *, save: bool = True) -> None:
        """
        Отмечает использование кода.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.used_count += 1
        self.last_used_at = timezone.now()

        if self.used_count >= self.max_uses:
            self.is_active = False

        if save:
            self.save(
                update_fields=[
                    "used_count",
                    "last_used_at",
                    "is_active",
                    "updated_at",
                ]
            )
