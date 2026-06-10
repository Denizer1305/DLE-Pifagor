from __future__ import annotations

from apps.organizations.constants import DEFAULT_TEACHER_REGISTRATION_CODE_TTL_DAYS
from apps.organizations.validators import (
    validate_future_datetime,
    validate_raw_teacher_registration_code,
)
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TeacherRegistrationCodeMixin(models.Model):
    """
    Миксин кода регистрации преподавателя в образовательную организацию.

    Код хранится только в виде хэша. Открытое значение кода не сохраняется.
    """

    teacher_registration_code_hash = models.CharField(
        _("Хэш кода регистрации преподавателя"),
        max_length=255,
        blank=True,
    )
    teacher_registration_code_is_active = models.BooleanField(
        _("Код регистрации преподавателя активен"),
        default=False,
    )
    teacher_registration_code_expires_at = models.DateTimeField(
        _("Код регистрации преподавателя истекает"),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def has_active_teacher_registration_code(self) -> bool:
        """
        Проверяет, есть ли активный код регистрации преподавателя.

        Returns:
            bool: True, если код задан, активен и не истёк.
        """

        if not self.teacher_registration_code_hash:
            return False

        if not self.teacher_registration_code_is_active:
            return False

        if self.teacher_registration_code_expires_at is None:
            return True

        return self.teacher_registration_code_expires_at > timezone.now()

    def set_teacher_registration_code(
        self,
        raw_code: str,
        *,
        expires_at=None,
        save: bool = True,
    ) -> None:
        """
        Устанавливает код регистрации преподавателя.

        Args:
            raw_code:
                Открытое значение кода.
            expires_at:
                Дата истечения кода.
            save:
                Нужно ли сразу сохранить объект.
        """

        validate_raw_teacher_registration_code(raw_code)

        if expires_at is None:
            expires_at = timezone.now() + timezone.timedelta(
                days=DEFAULT_TEACHER_REGISTRATION_CODE_TTL_DAYS,
            )

        self.teacher_registration_code_hash = make_password(raw_code)
        self.teacher_registration_code_is_active = True
        self.teacher_registration_code_expires_at = expires_at

        if save:
            self.save(
                update_fields=[
                    "teacher_registration_code_hash",
                    "teacher_registration_code_is_active",
                    "teacher_registration_code_expires_at",
                    "updated_at",
                ]
            )

    def clear_teacher_registration_code(self, *, save: bool = True) -> None:
        """
        Полностью очищает код регистрации преподавателя.

        Args:
            save:
                Нужно ли сразу сохранить объект.
        """

        self.teacher_registration_code_hash = ""
        self.teacher_registration_code_is_active = False
        self.teacher_registration_code_expires_at = None

        if save:
            self.save(
                update_fields=[
                    "teacher_registration_code_hash",
                    "teacher_registration_code_is_active",
                    "teacher_registration_code_expires_at",
                    "updated_at",
                ]
            )

    def disable_teacher_registration_code(self, *, save: bool = True) -> None:
        """
        Отключает код регистрации преподавателя без удаления хэша.

        Args:
            save:
                Нужно ли сразу сохранить объект.
        """

        self.teacher_registration_code_is_active = False

        if save:
            self.save(
                update_fields=[
                    "teacher_registration_code_is_active",
                    "updated_at",
                ]
            )

    def verify_teacher_registration_code(self, raw_code: str) -> bool:
        """
        Проверяет код регистрации преподавателя.

        Args:
            raw_code:
                Открытое значение кода.

        Returns:
            bool: True, если код корректен и активен.
        """

        if not raw_code:
            return False

        if not self.has_active_teacher_registration_code:
            return False

        return check_password(
            raw_code,
            self.teacher_registration_code_hash,
        )

    def clean(self) -> None:
        """
        Проверяет корректность срока действия кода.
        """

        super().clean()

        if self.teacher_registration_code_is_active:
            validate_future_datetime(
                value=self.teacher_registration_code_expires_at,
                field_name="teacher_registration_code_expires_at",
                message=(
                    "Активный код регистрации преподавателя "
                    "не может иметь истёкший срок действия."
                ),
            )
