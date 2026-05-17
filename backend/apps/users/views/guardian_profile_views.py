from __future__ import annotations

from apps.users.filters import GuardianLearnerFilter, GuardianProfileFilter
from apps.users.models import GuardianLearner, GuardianProfile
from apps.users.permissions import (
    CanGuardianAccessLearner,
    CanReviewGuardianLink,
    CanUpdateOwnProfile,
)
from apps.users.serializers import (
    GuardianLearnerSerializer,
    GuardianProfileSerializer,
    GuardianProfileUpdateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets


class GuardianProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet профилей родителей.
    """

    queryset = GuardianProfile.objects.select_related("user")
    filterset_class = GuardianProfileFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "occupation",
        "work_place",
    ]
    ordering_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
    ordering = [
        "-created_at",
    ]

    def get_serializer_class(self):
        """
        Возвращает serializer.

        Returns:
            Serializer: Класс serializer.
        """

        if self.action in {"update", "partial_update"}:
            return GuardianProfileUpdateSerializer

        return GuardianProfileSerializer

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"update", "partial_update"}:
            return [CanUpdateOwnProfile()]

        return [CanGuardianAccessLearner()]

    def get_queryset(self):
        """
        Ограничивает список профилей родителей.

        Returns:
            QuerySet: Профили родителей.
        """

        user = self.request.user

        if not user.is_authenticated:
            return GuardianProfile.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=user)


class GuardianLearnerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet связей родителей и учащихся.
    """

    queryset = GuardianLearner.objects.select_related(
        "guardian",
        "learner",
        "requested_by",
        "approved_by",
    )
    serializer_class = GuardianLearnerSerializer
    filterset_class = GuardianLearnerFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = [
        "id",
        "created_at",
        "updated_at",
        "approved_at",
    ]
    ordering = [
        "-created_at",
    ]

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"update", "partial_update"}:
            return [CanReviewGuardianLink()]

        return [CanGuardianAccessLearner()]

    def get_queryset(self):
        """
        Ограничивает список связей.

        Returns:
            QuerySet: Связи родителей и учащихся.
        """

        user = self.request.user

        if not user.is_authenticated:
            return GuardianLearner.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(guardian=user)
