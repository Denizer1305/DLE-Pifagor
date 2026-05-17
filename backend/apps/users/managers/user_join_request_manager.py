from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestStatus, JoinRequestType
from django.db import models
from django.utils import timezone


class UserJoinRequestQuerySet(models.QuerySet):
    """
    QuerySet для заявок пользователей на присоединение.
    """

    def pending(self):
        """
        Возвращает заявки, ожидающие проверки.

        Returns:
            QuerySet: Заявки со статусом pending.
        """

        return self.filter(status=JoinRequestStatus.PENDING)

    def approved(self):
        """
        Возвращает подтверждённые заявки.

        Returns:
            QuerySet: Заявки со статусом approved.
        """

        return self.filter(status=JoinRequestStatus.APPROVED)

    def rejected(self):
        """
        Возвращает отклонённые заявки.

        Returns:
            QuerySet: Заявки со статусом rejected.
        """

        return self.filter(status=JoinRequestStatus.REJECTED)

    def cancelled(self):
        """
        Возвращает отменённые заявки.

        Returns:
            QuerySet: Заявки со статусом cancelled.
        """

        return self.filter(status=JoinRequestStatus.CANCELLED)

    def expired(self):
        """
        Возвращает заявки со статусом expired.

        Returns:
            QuerySet: Истёкшие заявки.
        """

        return self.filter(status=JoinRequestStatus.EXPIRED)

    def expired_by_time(self):
        """
        Возвращает ожидающие заявки, срок которых истёк по времени.

        Returns:
            QuerySet: Заявки pending с expires_at в прошлом.
        """

        return self.pending().filter(
            expires_at__isnull=False,
            expires_at__lte=timezone.now(),
        )

    def teacher_to_organization(self):
        """
        Возвращает заявки преподавателей в организацию.

        Returns:
            QuerySet: Заявки типа teacher_to_organization.
        """

        return self.filter(
            request_type=JoinRequestType.TEACHER_TO_ORGANIZATION,
        )

    def learner_to_group(self):
        """
        Возвращает заявки учащихся в группу.

        Returns:
            QuerySet: Заявки типа learner_to_group.
        """

        return self.filter(
            request_type=JoinRequestType.LEARNER_TO_GROUP,
        )

    def guardian_to_learner(self):
        """
        Возвращает заявки родителей на связь с учащимся.

        Returns:
            QuerySet: Заявки типа guardian_to_learner.
        """

        return self.filter(
            request_type=JoinRequestType.GUARDIAN_TO_LEARNER,
        )

    def for_user(self, user):
        """
        Возвращает заявки конкретного пользователя.

        Args:
            user:
                Пользователь, который создал заявку.

        Returns:
            QuerySet: Заявки пользователя.
        """

        return self.filter(user=user)

    def for_target_user(self, user):
        """
        Возвращает заявки, где пользователь является целевым.

        Например, ребёнок в заявке родителя.

        Args:
            user:
                Целевой пользователь.

        Returns:
            QuerySet: Заявки по целевому пользователю.
        """

        return self.filter(target_user=user)

    def for_organization(self, organization):
        """
        Возвращает заявки образовательной организации.

        Args:
            organization:
                Образовательная организация.

        Returns:
            QuerySet: Заявки организации.
        """

        return self.filter(organization=organization)

    def for_department(self, department):
        """
        Возвращает заявки отделения.

        Args:
            department:
                Отделение.

        Returns:
            QuerySet: Заявки отделения.
        """

        return self.filter(department=department)

    def for_group(self, group):
        """
        Возвращает заявки группы.

        Args:
            group:
                Учебная группа.

        Returns:
            QuerySet: Заявки группы.
        """

        return self.filter(group=group)

    def waiting_for_reviewer(self, *, organization=None, department=None, group=None):
        """
        Возвращает заявки, ожидающие рассмотрения проверяющим.

        Args:
            organization:
                Образовательная организация.
            department:
                Отделение.
            group:
                Группа.

        Returns:
            QuerySet: Ожидающие заявки в заданном контексте.
        """

        queryset = self.pending()

        if organization is not None:
            queryset = queryset.filter(organization=organization)

        if department is not None:
            queryset = queryset.filter(department=department)

        if group is not None:
            queryset = queryset.filter(group=group)

        return queryset


class UserJoinRequestManager(models.Manager.from_queryset(UserJoinRequestQuerySet)):
    """
    Менеджер заявок пользователей.

    Полная логика подтверждения и отклонения заявок должна находиться
    в `users/services/user_join_request_services.py`.

    Manager содержит только удобные методы выборки.
    """

    def has_pending_request(
        self,
        *,
        user,
        request_type: str,
        organization=None,
        department=None,
        group=None,
        target_user=None,
    ) -> bool:
        """
        Проверяет, есть ли у пользователя активная ожидающая заявка.

        Args:
            user:
                Пользователь.
            request_type:
                Тип заявки.
            organization:
                Образовательная организация.
            department:
                Отделение.
            group:
                Группа.
            target_user:
                Целевой пользователь.

        Returns:
            bool: True, если ожидающая заявка уже существует.
        """

        queryset = (
            self.get_queryset()
            .pending()
            .filter(
                user=user,
                request_type=request_type,
            )
        )

        if organization is not None:
            queryset = queryset.filter(organization=organization)

        if department is not None:
            queryset = queryset.filter(department=department)

        if group is not None:
            queryset = queryset.filter(group=group)

        if target_user is not None:
            queryset = queryset.filter(target_user=target_user)

        return queryset.exists()
