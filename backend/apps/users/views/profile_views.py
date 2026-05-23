from __future__ import annotations

from apps.users.filters import ProfileFilter
from apps.users.models import Profile
from apps.users.permissions import (
    CanModerateProfile,
    CanUpdateOwnProfile,
    CanViewProfile,
)
from apps.users.serializers import (
    AvatarModerationSerializer,
    CurrentProfileAvatarSerializer,
    CurrentProfileSerializer,
    CurrentProfileUpdateSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
)
from apps.users.services import (
    build_current_profile_payload,
    delete_current_profile_avatar,
    moderate_avatar,
    submit_avatar_for_moderation,
    update_current_profile,
    update_current_profile_avatar,
)
from apps.users.services.current_profile.locations import suggest_cities
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet базовых профилей пользователей.
    """

    queryset = Profile.objects.select_related("user")
    filterset_class = ProfileFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "city",
        "about",
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
        Возвращает serializer в зависимости от действия.

        Returns:
            Serializer: Класс serializer.
        """

        if self.action in {"update", "partial_update"}:
            return ProfileUpdateSerializer

        if self.action == "moderate_avatar":
            return AvatarModerationSerializer

        return ProfileSerializer

    def get_permissions(self):
        """
        Возвращает permissions в зависимости от действия.

        Returns:
            list: Список permission instances.
        """

        if self.action in {"update", "partial_update", "submit_avatar"}:
            return [CanUpdateOwnProfile()]

        if self.action == "moderate_avatar":
            return [CanModerateProfile()]

        return [CanViewProfile()]

    def get_queryset(self):
        """
        Ограничивает список профилей.

        Returns:
            QuerySet: Профили.
        """

        user = self.request.user

        if not user.is_authenticated:
            return Profile.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=user)

    @action(detail=True, methods=["post"], url_path="submit-avatar")
    def submit_avatar(self, request, pk=None):
        """
        Отправляет аватар на модерацию.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID профиля.

        Returns:
            Response: Обновлённый профиль.
        """

        profile = self.get_object()
        profile = submit_avatar_for_moderation(profile=profile)

        return Response(ProfileSerializer(profile).data)

    @action(detail=True, methods=["post"], url_path="moderate-avatar")
    def moderate_avatar(self, request, pk=None):
        """
        Модерирует аватар пользователя.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID профиля.

        Returns:
            Response: Обновлённый профиль.
        """

        profile = self.get_object()
        serializer = AvatarModerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = moderate_avatar(
            profile=profile,
            moderator=request.user,
            is_approved=serializer.validated_data["is_approved"],
            comment=serializer.validated_data.get("comment", ""),
            request=request,
        )

        return Response(ProfileSerializer(profile).data)

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """
        Возвращает агрегированные данные текущего профиля.
        """

        payload = build_current_profile_payload(user=request.user)

        return Response(
            CurrentProfileSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me/edit",
        permission_classes=[IsAuthenticated],
    )
    def me_edit(self, request):
        """
        Возвращает или обновляет данные формы редактирования текущего профиля.
        """

        if request.method == "GET":
            payload = build_current_profile_payload(user=request.user)

            return Response(
                CurrentProfileSerializer(payload).data,
                status=status.HTTP_200_OK,
            )

        serializer = CurrentProfileUpdateSerializer(
            data=request.data,
            partial=True,
            context={"primary_email": request.user.email},
        )
        serializer.is_valid(raise_exception=True)

        payload = update_current_profile(
            user=request.user,
            data=serializer.validated_data,
            request=request,
        )

        return Response(
            CurrentProfileSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post", "delete"],
        url_path="me/avatar",
        permission_classes=[IsAuthenticated],
    )
    def me_avatar(self, request):
        """
        Загружает или удаляет аватар текущего пользователя.
        """

        if request.method == "DELETE":
            payload = delete_current_profile_avatar(
                user=request.user,
                request=request,
            )

            return Response(
                CurrentProfileSerializer(payload).data,
                status=status.HTTP_200_OK,
            )

        serializer = CurrentProfileAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = update_current_profile_avatar(
            user=request.user,
            avatar=serializer.validated_data["avatar"],
            request=request,
        )

        return Response(
            CurrentProfileSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="me/city-suggestions",
        permission_classes=[IsAuthenticated],
    )
    def me_city_suggestions(self, request):
        query = request.query_params.get("query", "")

        return Response(
            {"suggestions": suggest_cities(query=query)},
            status=status.HTTP_200_OK,
        )
