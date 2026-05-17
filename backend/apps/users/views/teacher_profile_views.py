from __future__ import annotations

from apps.users.filters import TeacherProfileFilter
from apps.users.models import TeacherProfile
from apps.users.permissions import (
    CanReviewTeacherProfile,
    CanUpdateOwnProfile,
    CanViewProfile,
)
from apps.users.serializers import (
    PublicTeacherProfileSerializer,
    TeacherProfileSerializer,
    TeacherProfileUpdateSerializer,
)
from apps.users.services import verify_teacher_profile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class TeacherProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet профилей преподавателей.
    """

    queryset = TeacherProfile.objects.select_related(
        "user",
        "organization",
        "department",
        "verified_by",
    )
    filterset_class = TeacherProfileFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "position",
        "public_title",
    ]
    ordering_fields = [
        "id",
        "experience_years",
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
            return TeacherProfileUpdateSerializer

        if self.action == "public":
            return PublicTeacherProfileSerializer

        return TeacherProfileSerializer

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"update", "partial_update"}:
            return [CanUpdateOwnProfile()]

        if self.action == "verify":
            return [CanReviewTeacherProfile()]

        return [CanViewProfile()]

    def get_queryset(self):
        """
        Ограничивает список преподавателей.

        Returns:
            QuerySet: Профили преподавателей.
        """

        user = self.request.user

        if self.action == "public":
            return self.queryset.filter(
                is_public=True,
                show_on_teachers_page=True,
            )

        if not user.is_authenticated:
            return TeacherProfile.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=user)

    @action(detail=False, methods=["get"])
    def public(self, request):
        """
        Возвращает публичные профили преподавателей.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Список публичных преподавателей.
        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = PublicTeacherProfileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PublicTeacherProfileSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        """
        Подтверждает профиль преподавателя.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID профиля.

        Returns:
            Response: Обновлённый профиль.
        """

        profile = self.get_object()
        profile = verify_teacher_profile(
            profile=profile,
            verified_by=request.user,
            request=request,
        )

        return Response(TeacherProfileSerializer(profile).data)
