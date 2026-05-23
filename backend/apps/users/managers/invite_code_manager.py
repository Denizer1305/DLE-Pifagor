from __future__ import annotations

from apps.users.constants.onboarding import InviteCodePurpose
from django.db import models
from django.utils import timezone


class InviteCodeQuerySet(models.QuerySet):
    """
    QuerySet для временных кодов приглашения.
    """

    def active(self):
        """
        Возвращает активные коды.

        Returns:
            QuerySet: Активные коды.
        """

        return self.filter(is_active=True)

    def expired(self):
        """
        Возвращает истёкшие коды.

        Returns:
            QuerySet: Коды, срок действия которых истёк.
        """

        return self.filter(expires_at__lte=timezone.now())

    def not_expired(self):
        """
        Возвращает неистёкшие коды.

        Returns:
            QuerySet: Коды, срок действия которых ещё не истёк.
        """

        return self.filter(expires_at__gt=timezone.now())

    def available(self):
        """
        Возвращает коды, доступные для использования.

        Код доступен, если:
            - активен;
            - срок действия не истёк;
            - лимит использований не достигнут.

        Returns:
            QuerySet: Доступные коды.
        """

        return (
            self.active()
            .not_expired()
            .filter(
                used_count__lt=models.F("max_uses"),
            )
        )

    def for_purpose(self, purpose: str):
        """
        Возвращает коды по назначению.

        Args:
            purpose:
                Назначение кода.

        Returns:
            QuerySet: Коды с указанным назначением.
        """

        return self.filter(purpose=purpose)

    def for_teacher_registration(self):
        """
        Возвращает коды регистрации преподавателя.

        Returns:
            QuerySet: Коды для регистрации преподавателя.
        """

        return self.for_purpose(InviteCodePurpose.TEACHER_REGISTRATION)

    def for_guardian_curator_link(self):
        """
        Возвращает коды куратора для связи родителя и учащегося.

        Returns:
            QuerySet: Коды куратора.
        """

        return self.for_purpose(InviteCodePurpose.GUARDIAN_LINK_CURATOR)

    def for_guardian_learner_link(self):
        """
        Возвращает коды учащегося для связи родителя и учащегося.

        Returns:
            QuerySet: Коды учащегося.
        """

        return self.for_purpose(InviteCodePurpose.GUARDIAN_LINK_LEARNER)

    def for_organization(self, organization):
        """
        Возвращает коды образовательной организации.

        Args:
            organization:
                Образовательная организация.

        Returns:
            QuerySet: Коды организации.
        """

        return self.filter(organization=organization)

    def for_department(self, department):
        """
        Возвращает коды отделения.

        Args:
            department:
                Отделение.

        Returns:
            QuerySet: Коды отделения.
        """

        return self.filter(department=department)

    def for_group(self, group):
        """
        Возвращает коды группы.

        Args:
            group:
                Учебная группа.

        Returns:
            QuerySet: Коды группы.
        """

        return self.filter(group=group)

    def for_target_user(self, user):
        """
        Возвращает коды, выданные конкретному целевому пользователю.

        Args:
            user:
                Целевой пользователь.

        Returns:
            QuerySet: Коды пользователя.
        """

        return self.filter(target_user=user)


class InviteCodeManager(models.Manager.from_queryset(InviteCodeQuerySet)):
    """
    Менеджер временных кодов приглашения.

    Полная логика генерации и проверки кодов должна находиться
    в `users/services/invite_code_services.py`.

    Manager содержит только удобные методы выборки.
    """

    def find_available_by_hash(self, code_hash: str):
        """
        Ищет доступный код по хешу.

        Args:
            code_hash:
                Хеш кода.

        Returns:
            InviteCode | None: Найденный код или None.
        """

        if not code_hash:
            return None

        return self.get_queryset().available().filter(code_hash=code_hash).first()
