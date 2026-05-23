from __future__ import annotations

from apps.core.models import LifecycleModel
from apps.core.validators import validate_birth_date_not_future, validate_phone_number
from apps.users.constants.lifecycle import UserStatus
from apps.users.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin, LifecycleModel):
    """
    Кастомная модель пользователя ЦОС «Пифагор».

    Основные правила:
        - email используется как основной логин;
        - username не используется;
        - phone обязателен для всех аккаунтов;
        - пользователь может иметь несколько ролей;
        - ребёнок младше 14 лет тоже имеет отдельный User;
        - до 14 лет аккаунтом ребёнка управляет родитель;
        - самостоятельный вход можно активировать позже.

    Важно:
        Эта модель должна быть указана в settings:
            AUTH_USER_MODEL = "users.User"
    """

    email = models.EmailField(
        _("Email"),
        unique=True,
        db_index=True,
    )
    backup_email = models.EmailField(
        _("Резервный email"),
        blank=True,
        default="",
    )
    phone = models.CharField(
        _("Телефон"),
        max_length=32,
        unique=True,
        db_index=True,
        validators=[validate_phone_number],
    )

    first_name = models.CharField(
        _("Имя"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=150,
    )
    middle_name = models.CharField(
        _("Отчество"),
        max_length=150,
        blank=True,
    )
    birth_date = models.DateField(
        _("Дата рождения"),
        blank=True,
        null=True,
        validators=[validate_birth_date_not_future],
    )

    status = models.CharField(
        _("Статус аккаунта"),
        max_length=32,
        choices=UserStatus.choices,
        default=UserStatus.PENDING_EMAIL,
        db_index=True,
    )

    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )
    is_staff = models.BooleanField(
        _("Доступ в административную панель"),
        default=False,
    )

    is_email_verified = models.BooleanField(
        _("Email подтверждён"),
        default=False,
    )
    email_verified_at = models.DateTimeField(
        _("Дата подтверждения email"),
        blank=True,
        null=True,
    )

    is_phone_verified = models.BooleanField(
        _("Телефон подтверждён"),
        default=False,
    )
    phone_verified_at = models.DateTimeField(
        _("Дата подтверждения телефона"),
        blank=True,
        null=True,
    )

    is_login_allowed = models.BooleanField(
        _("Самостоятельный вход разрешён"),
        default=True,
    )
    account_managed_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="managed_accounts",
        verbose_name=_("Аккаунтом управляет"),
        blank=True,
        null=True,
        help_text=_("Используется для аккаунтов детей младше 14 лет."),
    )

    login_available_from = models.DateField(
        _("Самостоятельный вход доступен с"),
        blank=True,
        null=True,
    )
    login_activation_requested_at = models.DateTimeField(
        _("Дата запроса самостоятельного входа"),
        blank=True,
        null=True,
    )
    login_activated_at = models.DateTimeField(
        _("Дата активации самостоятельного входа"),
        blank=True,
        null=True,
    )

    scheduled_for_deletion_at = models.DateTimeField(
        _("Дата планируемого удаления"),
        blank=True,
        null=True,
    )
    anonymized_at = models.DateTimeField(
        _("Дата анонимизации"),
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "phone",
        "first_name",
        "last_name",
    ]

    class Meta:
        db_table = "users_user"
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("last_name", "first_name", "email")
        indexes = [
            models.Index(fields=["email"], name="users_user_email_idx"),
            models.Index(fields=["phone"], name="users_user_phone_idx"),
            models.Index(fields=["status"], name="users_user_status_idx"),
            models.Index(fields=["is_active"], name="users_user_active_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя.

        Returns:
            str: ФИО пользователя или email.
        """

        return self.get_full_name() or self.email

    def clean(self) -> None:
        """
        Нормализует поля пользователя перед сохранением.
        """

        super().clean()

        if self.email:
            self.email = self.email.strip().lower()

        if self.backup_email:
            self.backup_email = self.backup_email.strip().lower()

        if self.phone:
            self.phone = self.phone.strip()

        if self.first_name:
            self.first_name = self.first_name.strip()

        if self.last_name:
            self.last_name = self.last_name.strip()

        if self.middle_name:
            self.middle_name = self.middle_name.strip()

    def get_full_name(self) -> str:
        """
        Возвращает полное имя пользователя.

        Returns:
            str: Фамилия, имя и отчество.
        """

        parts = [
            self.last_name,
            self.first_name,
            self.middle_name,
        ]

        return " ".join(part for part in parts if part).strip()

    def get_short_name(self) -> str:
        """
        Возвращает краткое имя пользователя.

        Returns:
            str: Имя пользователя или email.
        """

        return self.first_name or self.email

    @property
    def is_pending_email(self) -> bool:
        """
        Проверяет, ожидает ли пользователь подтверждения email.

        Returns:
            bool: True, если пользователь ожидает подтверждения email.
        """

        return self.status == UserStatus.PENDING_EMAIL

    @property
    def is_blocked(self) -> bool:
        """
        Проверяет, заблокирован ли пользователь.

        Returns:
            bool: True, если пользователь заблокирован.
        """

        return self.status == UserStatus.BLOCKED

    @property
    def is_anonymized(self) -> bool:
        """
        Проверяет, анонимизирован ли пользователь.

        Returns:
            bool: True, если пользователь анонимизирован.
        """

        return self.status == UserStatus.ANONYMIZED or self.anonymized_at is not None

    def mark_email_verified(self, *, save: bool = True) -> None:
        """
        Отмечает email пользователя как подтверждённый.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.is_email_verified = True
        self.email_verified_at = timezone.now()

        if self.status == UserStatus.PENDING_EMAIL:
            self.status = UserStatus.PENDING_REVIEW

        if save:
            self.save(
                update_fields=[
                    "is_email_verified",
                    "email_verified_at",
                    "status",
                    "updated_at",
                ]
            )

    def mark_phone_verified(self, *, save: bool = True) -> None:
        """
        Отмечает телефон пользователя как подтверждённый.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.is_phone_verified = True
        self.phone_verified_at = timezone.now()

        if save:
            self.save(
                update_fields=[
                    "is_phone_verified",
                    "phone_verified_at",
                    "updated_at",
                ]
            )

    def activate(self, *, save: bool = True) -> None:
        """
        Активирует аккаунт пользователя.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserStatus.ACTIVE
        self.is_active = True

        if save:
            self.save(update_fields=["status", "is_active", "updated_at"])

    def block(self, *, save: bool = True) -> None:
        """
        Блокирует аккаунт пользователя.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserStatus.BLOCKED
        self.is_active = False

        if save:
            self.save(update_fields=["status", "is_active", "updated_at"])

    def schedule_for_deletion(self, *, when, save: bool = True) -> None:
        """
        Планирует удаление или анонимизацию пользователя.

        Args:
            when:
                Дата и время запланированного удаления.
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserStatus.SCHEDULED_FOR_DELETION
        self.scheduled_for_deletion_at = when
        self.is_active = False

        if save:
            self.save(
                update_fields=[
                    "status",
                    "scheduled_for_deletion_at",
                    "is_active",
                    "updated_at",
                ]
            )

    def mark_anonymized(self, *, save: bool = True) -> None:
        """
        Помечает аккаунт как анонимизированный.

        Важно:
            Само обезличивание персональных данных должно выполняться
            в сервисном слое, а модель только фиксирует состояние.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserStatus.ANONYMIZED
        self.is_active = False
        self.anonymized_at = timezone.now()

        if save:
            self.save(
                update_fields=[
                    "status",
                    "is_active",
                    "anonymized_at",
                    "updated_at",
                ]
            )
