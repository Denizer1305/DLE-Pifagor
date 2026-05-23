from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.managers import RoleManager, UserRoleManager
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Role(TimeStampedModel):
    """
    Справочник системных ролей.

    Роли не заменяют Django-поля is_staff и is_superuser.
    Они используются для бизнес-доступа внутри ЦОС «Пифагор».
    """

    objects = RoleManager()

    code = models.CharField(
        _("Код роли"),
        max_length=64,
        choices=RoleCode.choices,
        unique=True,
        db_index=True,
    )
    label = models.CharField(
        _("Название роли"),
        max_length=150,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    is_system = models.BooleanField(
        _("Системная роль"),
        default=True,
    )
    is_active = models.BooleanField(
        _("Активна"),
        default=True,
    )
    sort_order = models.PositiveIntegerField(
        _("Порядок сортировки"),
        default=100,
    )

    class Meta:
        db_table = "users_role"
        verbose_name = _("Роль")
        verbose_name_plural = _("Роли")
        ordering = ("sort_order", "label")

    def __str__(self) -> str:
        """
        Возвращает строковое представление роли.

        Returns:
            str: Название и код роли.
        """

        return f"{self.label} ({self.code})"


class UserRole(TimeStampedModel):
    """
    Назначенная роль пользователя.

    Роль может быть привязана:
        - ко всей платформе;
        - к образовательной организации;
        - к отделению;
        - к группе.

    Примеры:
        - superadmin без организации;
        - director в организации;
        - department_head в отделении;
        - curator в группе;
        - learner в группе.
    """

    objects = UserRoleManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name=_("Пользователь"),
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="user_roles",
        verbose_name=_("Роль"),
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name=_("Образовательная организация"),
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="user_roles",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.SET_NULL,
        related_name="user_roles",
        verbose_name=_("Группа"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Статус роли"),
        max_length=32,
        choices=UserRoleStatus.choices,
        default=UserRoleStatus.PENDING,
        db_index=True,
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_user_roles",
        verbose_name=_("Назначил"),
        blank=True,
        null=True,
    )
    assigned_at = models.DateTimeField(
        _("Дата назначения"),
        default=timezone.now,
    )

    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="revoked_user_roles",
        verbose_name=_("Отозвал"),
        blank=True,
        null=True,
    )
    revoked_at = models.DateTimeField(
        _("Дата отзыва"),
        blank=True,
        null=True,
    )
    revoke_reason = models.TextField(
        _("Причина отзыва"),
        blank=True,
    )

    class Meta:
        db_table = "users_user_role"
        verbose_name = _("Роль пользователя")
        verbose_name_plural = _("Роли пользователей")
        ordering = ("user", "role")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                condition=models.Q(
                    organization__isnull=True,
                    department__isnull=True,
                    group__isnull=True,
                ),
                name="users_user_role_unique_platform",
            ),
            models.UniqueConstraint(
                fields=["user", "role", "organization"],
                condition=models.Q(
                    organization__isnull=False,
                    department__isnull=True,
                    group__isnull=True,
                ),
                name="users_user_role_unique_org",
            ),
            models.UniqueConstraint(
                fields=["user", "role", "organization", "department"],
                condition=models.Q(
                    organization__isnull=False,
                    department__isnull=False,
                    group__isnull=True,
                ),
                name="users_user_role_unique_department",
            ),
            models.UniqueConstraint(
                fields=["user", "role", "organization", "group"],
                condition=models.Q(
                    organization__isnull=False,
                    group__isnull=False,
                ),
                name="users_user_role_unique_group",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"], name="users_ur_user_status_idx"),
            models.Index(fields=["role", "status"], name="users_ur_role_status_idx"),
            models.Index(fields=["organization"], name="users_ur_org_idx"),
            models.Index(fields=["department"], name="users_ur_dept_idx"),
            models.Index(fields=["group"], name="users_ur_group_idx"),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление назначенной роли.

        Returns:
            str: Пользователь и роль.
        """

        return f"{self.user} — {self.role}"

    @property
    def is_active_role(self) -> bool:
        """
        Проверяет, активна ли роль пользователя.

        Returns:
            bool: True, если роль активна.
        """

        return self.status == UserRoleStatus.ACTIVE

    def approve(self, *, save: bool = True) -> None:
        """
        Подтверждает роль пользователя.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserRoleStatus.ACTIVE

        if save:
            self.save(update_fields=["status", "updated_at"])

    def reject(self, *, save: bool = True) -> None:
        """
        Отклоняет роль пользователя.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserRoleStatus.REJECTED

        if save:
            self.save(update_fields=["status", "updated_at"])

    def revoke(self, *, user=None, reason: str = "", save: bool = True) -> None:
        """
        Отзывает роль пользователя.

        Args:
            user:
                Пользователь, который отозвал роль.
            reason:
                Причина отзыва.
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.status = UserRoleStatus.REVOKED
        self.revoked_by = user
        self.revoked_at = timezone.now()
        self.revoke_reason = reason or ""

        if save:
            self.save(
                update_fields=[
                    "status",
                    "revoked_by",
                    "revoked_at",
                    "revoke_reason",
                    "updated_at",
                ]
            )
