from __future__ import annotations

from apps.users.filters import LearnerProfileFilter
from apps.users.models import LearnerProfile
from apps.users.permissions import (
    CanGuardianViewLearnerProfile,
    CanReviewLearnerProfile,
    CanUpdateOwnProfile,
)
from apps.users.serializers import (
    JoinRequestReviewSerializer,
    LearnerProfileSerializer,
    LearnerProfileUpdateSerializer,
    SubmitLearnerGroupRequestSerializer,
)
from apps.users.services import submit_learner_group_request, verify_learner_profile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class LearnerProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet профилей учащихся.
    """

    queryset = LearnerProfile.objects.select_related(
        "user",
        "organization",
        "department",
        "group",
        "curator",
        "created_by_guardian",
        "verified_by",
    )
    filterset_class = LearnerProfileFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "learner_code",
    ]
    ordering_fields = [
        "id",
        "admission_year",
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
            return LearnerProfileUpdateSerializer

        if self.action == "submit_group_request":
            return SubmitLearnerGroupRequestSerializer

        if self.action == "verify":
            return JoinRequestReviewSerializer

        return LearnerProfileSerializer

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"update", "partial_update", "submit_group_request"}:
            return [CanUpdateOwnProfile()]

        if self.action == "verify":
            return [CanReviewLearnerProfile()]

        return [CanGuardianViewLearnerProfile()]

    def get_queryset(self):
        """
        Ограничивает список профилей учащихся.

        Returns:
            QuerySet: Профили учащихся.
        """

        user = self.request.user

        if not user.is_authenticated:
            return LearnerProfile.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=user)

    @action(detail=True, methods=["post"], url_path="submit-group-request")
    def submit_group_request(self, request, pk=None):
        """
        Отправляет заявку учащегося в группу.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID профиля.

        Returns:
            Response: Созданная заявка.
        """

        profile = self.get_object()
        serializer = SubmitLearnerGroupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        join_request = submit_learner_group_request(
            user=profile.user,
            organization=serializer.validated_data.get("organization"),
            department=serializer.validated_data.get("department"),
            group=serializer.validated_data.get("group"),
            curator=serializer.validated_data.get("curator"),
            request=request,
        )

        from apps.users.serializers import UserJoinRequestSerializer

        return Response(UserJoinRequestSerializer(join_request).data)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        """
        Подтверждает профиль учащегося.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID профиля.

        Returns:
            Response: Обновлённый профиль.
        """

        profile = self.get_object()
        profile = verify_learner_profile(
            profile=profile,
            verified_by=request.user,
            request=request,
        )

        return Response(LearnerProfileSerializer(profile).data)
