from __future__ import annotations

from apps.organizations.constants import DEFAULT_GROUP_JOIN_CODE_TTL_DAYS
from apps.organizations.validators import (
    validate_future_datetime,
    validate_raw_group_join_code,
)
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GroupJoinCodeMixin(models.Model):
    """
    Миксин кода вступления в учебную группу.

    Код хранится только в виде хэша. Открытое значение кода не сохраняется.
    """

    join_code_hash = models.CharField(
        _("Хэш кода вступления в группу"),
        max_length=255,
        blank=True,
    )
    join_code_is_active = models.BooleanField(
        _("Код вступления в группу активен"),
        default=False,
    )
    join_code_expires_at = models.DateTimeField(
        _("Код вступления в группу истекает"),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def has_active_join_code(self) -> bool:
        """
        Проверяет, есть ли активный код вступления в группу.

        Returns:
            bool: True, если код задан, активен и не истёк.
        """

        if not self.join_code_hash:
            return False

        if not self.join_code_is_active:
            return False

        if self.join_code_expires_at is None:
            return True

        return self.join_code_expires_at > timezone.now()

    def set_join_code(
        self,
        raw_code: str,
        *,
        expires_at=None,
        save: bool = True,
    ) -> None:
        """
        Устанавливает код вступления в группу.

        Args:
            raw_code:
                Открытое значение кода.
            expires_at:
                Дата истечения кода.
            save:
                Нужно ли сразу сохранить объект.
        """

        validate_raw_group_join_code(raw_code)

        if expires_at is None:
            expires_at = timezone.now() + timezone.timedelta(
                days=DEFAULT_GROUP_JOIN_CODE_TTL_DAYS,
            )

        self.join_code_hash = make_password(raw_code)
        self.join_code_is_active = True
        self.join_code_expires_at = expires_at

        if save:
            self.save(
                update_fields=[
                    "join_code_hash",
                    "join_code_is_active",
                    "join_code_expires_at",
                    "updated_at",
                ]
            )

    def clear_join_code(self, *, save: bool = True) -> None:
        """
        Полностью очищает код вступления в группу.

        Args:
            save:
                Нужно ли сразу сохранить объект.
        """

        self.join_code_hash = ""
        self.join_code_is_active = False
        self.join_code_expires_at = None

        if save:
            self.save(
                update_fields=[
                    "join_code_hash",
                    "join_code_is_active",
                    "join_code_expires_at",
                    "updated_at",
                ]
            )

    def disable_join_code(self, *, save: bool = True) -> None:
        """
        Отключает код вступления в группу без удаления хэша.

        Args:
            save:
                Нужно ли сразу сохранить объект.
        """

        self.join_code_is_active = False

        if save:
            self.save(
                update_fields=[
                    "join_code_is_active",
                    "updated_at",
                ]
            )

    def verify_join_code(self, raw_code: str) -> bool:
        """
        Проверяет код вступления в группу.

        Args:
            raw_code:
                Открытое значение кода.

        Returns:
            bool: True, если код корректен и активен.
        """

        if not raw_code:
            return False

        if not self.has_active_join_code:
            return False

        return check_password(
            raw_code,
            self.join_code_hash,
        )

    def clean(self) -> None:
        """
        Проверяет корректность срока действия кода.
        """

        super().clean()

        if self.join_code_is_active:
            validate_future_datetime(
                value=self.join_code_expires_at,
                field_name="join_code_expires_at",
                message=(
                    "Активный код вступления в группу "
                    "не может иметь истёкший срок действия."
                ),
            )
