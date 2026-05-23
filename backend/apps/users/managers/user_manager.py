from __future__ import annotations

from typing import Any

from apps.users.constants.lifecycle import UserStatus
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserQuerySet(models.QuerySet):
    """
    QuerySet для модели User.

    Содержит часто используемые выборки пользователей:
        - активные пользователи;
        - пользователи на проверке;
        - заблокированные;
        - архивные;
        - запланированные к удалению;
        - анонимизированные;
        - пользователи с подтверждённым email.
    """

    def active(self):
        """
        Возвращает активных пользователей.

        Returns:
            QuerySet: Пользователи со статусом active и is_active=True.
        """

        return self.filter(
            status=UserStatus.ACTIVE,
            is_active=True,
        )

    def pending_email(self):
        """
        Возвращает пользователей, ожидающих подтверждения email.

        Returns:
            QuerySet: Пользователи со статусом pending_email.
        """

        return self.filter(status=UserStatus.PENDING_EMAIL)

    def pending_review(self):
        """
        Возвращает пользователей, ожидающих проверки.

        Returns:
            QuerySet: Пользователи со статусом pending_review.
        """

        return self.filter(status=UserStatus.PENDING_REVIEW)

    def rejected(self):
        """
        Возвращает отклонённых пользователей.

        Returns:
            QuerySet: Пользователи со статусом rejected.
        """

        return self.filter(status=UserStatus.REJECTED)

    def blocked(self):
        """
        Возвращает заблокированных пользователей.

        Returns:
            QuerySet: Пользователи со статусом blocked.
        """

        return self.filter(status=UserStatus.BLOCKED)

    def archived(self):
        """
        Возвращает архивированных пользователей.

        Returns:
            QuerySet: Пользователи со статусом archived.
        """

        return self.filter(status=UserStatus.ARCHIVED)

    def scheduled_for_deletion(self):
        """
        Возвращает пользователей, запланированных к удалению или анонимизации.

        Returns:
            QuerySet: Пользователи со статусом scheduled_for_deletion.
        """

        return self.filter(status=UserStatus.SCHEDULED_FOR_DELETION)

    def anonymized(self):
        """
        Возвращает анонимизированных пользователей.

        Returns:
            QuerySet: Пользователи со статусом anonymized.
        """

        return self.filter(status=UserStatus.ANONYMIZED)

    def email_verified(self):
        """
        Возвращает пользователей с подтверждённым email.

        Returns:
            QuerySet: Пользователи с is_email_verified=True.
        """

        return self.filter(is_email_verified=True)

    def phone_verified(self):
        """
        Возвращает пользователей с подтверждённым телефоном.

        Returns:
            QuerySet: Пользователи с is_phone_verified=True.
        """

        return self.filter(is_phone_verified=True)

    def login_allowed(self):
        """
        Возвращает пользователей, которым разрешён самостоятельный вход.

        Returns:
            QuerySet: Пользователи с is_login_allowed=True.
        """

        return self.filter(is_login_allowed=True)

    def managed_accounts(self):
        """
        Возвращает управляемые аккаунты.

        Например, аккаунты детей младше 14 лет,
        которыми управляет родитель или законный представитель.

        Returns:
            QuerySet: Пользователи с заполненным account_managed_by.
        """

        return self.filter(account_managed_by__isnull=False)

    def by_email(self, email: str):
        """
        Ищет пользователя по email.

        Args:
            email:
                Email пользователя.

        Returns:
            QuerySet: Пользователи с указанным email.
        """

        if not email:
            return self.none()

        return self.filter(email=email.strip().lower())

    def by_phone(self, phone: str):
        """
        Ищет пользователя по телефону.

        Args:
            phone:
                Телефон пользователя.

        Returns:
            QuerySet: Пользователи с указанным телефоном.
        """

        if not phone:
            return self.none()

        return self.filter(phone=phone.strip())


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    """
    Менеджер кастомной модели пользователя.

    Пользователь в ЦОС «Пифагор» авторизуется по email.
    Username не используется.

    Менеджер отвечает только за базовое создание пользователя
    и суперпользователя. Полные сценарии регистрации должны жить
    в `users/services/registration_services.py`.
    """

    use_in_migrations = True

    def normalize_email(self, email: str | None) -> str:
        """
        Нормализует email пользователя.

        Args:
            email:
                Email пользователя.

        Returns:
            str: Нормализованный email.
        """

        normalized_email = super().normalize_email(email)

        return normalized_email.strip().lower() if normalized_email else ""

    def create_user(
        self,
        email: str,
        phone: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Создаёт обычного пользователя.

        Args:
            email:
                Email пользователя. Используется как основной логин.
            phone:
                Телефон пользователя. Обязателен при регистрации.
            password:
                Пароль пользователя.
            **extra_fields:
                Дополнительные поля модели User.

        Returns:
            User: Созданный пользователь.

        Raises:
            ValueError: Если email или phone не переданы.
        """

        if not email:
            raise ValueError(_("Email обязателен."))

        if not phone:
            raise ValueError(_("Телефон обязателен."))

        email = self.normalize_email(email)
        phone = phone.strip()

        extra_fields.setdefault("status", UserStatus.PENDING_EMAIL)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_email_verified", False)
        extra_fields.setdefault("is_phone_verified", False)
        extra_fields.setdefault("is_login_allowed", True)

        user = self.model(
            email=email,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email: str,
        phone: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Создаёт суперпользователя Django.

        Args:
            email:
                Email суперпользователя.
            phone:
                Телефон суперпользователя.
            password:
                Пароль суперпользователя.
            **extra_fields:
                Дополнительные поля модели User.

        Returns:
            User: Созданный суперпользователь.

        Raises:
            ValueError: Если is_staff или is_superuser не равны True.
        """

        extra_fields.setdefault("status", UserStatus.ACTIVE)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_email_verified", True)
        extra_fields.setdefault("is_phone_verified", True)
        extra_fields.setdefault("is_login_allowed", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_superuser=True."))

        return self.create_user(
            email=email,
            phone=phone,
            password=password,
            **extra_fields,
        )

    def create_managed_child_user(
        self,
        *,
        email: str,
        phone: str,
        password: str | None = None,
        account_managed_by,
        **extra_fields: Any,
    ):
        """
        Создаёт управляемый аккаунт ребёнка младше 14 лет.

        Аккаунт ребёнка имеет собственный User, email и phone,
        но самостоятельный вход изначально запрещён.

        Args:
            email:
                Email ребёнка.
            phone:
                Телефон ребёнка.
            password:
                Пароль. Может быть временным или не использоваться до активации входа.
            account_managed_by:
                Родитель или законный представитель, управляющий аккаунтом.
            **extra_fields:
                Дополнительные поля модели User.

        Returns:
            User: Созданный управляемый аккаунт ребёнка.
        """

        extra_fields.setdefault("status", UserStatus.PENDING_REVIEW)
        extra_fields.setdefault("is_login_allowed", False)
        extra_fields.setdefault("account_managed_by", account_managed_by)

        return self.create_user(
            email=email,
            phone=phone,
            password=password,
            **extra_fields,
        )
