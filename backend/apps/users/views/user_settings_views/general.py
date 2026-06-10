from apps.users.serializers.user_settings_serializers import (
    AppearanceSettingsUpdateSerializer,
    NotificationSettingsUpdateSerializer,
    UserSettingsPayloadSerializer,
    UserSettingsUpdateSerializer,
)
from apps.users.services import (
    build_appearance_settings_payload,
    build_notification_settings_payload,
    build_settings_payload,
    update_all_settings,
    update_appearance_settings,
    update_notification_settings,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserSettingsGeneralMixin:
    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        settings_obj = self.get_settings_obj()

        if request.method == "GET":
            payload = build_settings_payload(settings_obj=settings_obj)
            return Response(
                UserSettingsPayloadSerializer(payload).data,
                status=status.HTTP_200_OK,
            )

        serializer = UserSettingsUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        payload = update_all_settings(
            settings_obj=settings_obj,
            data=serializer.validated_data,
        )
        return Response(
            UserSettingsPayloadSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get", "patch"], url_path="me/appearance")
    def appearance(self, request):
        settings_obj = self.get_settings_obj()

        if request.method == "GET":
            return Response(
                build_appearance_settings_payload(settings_obj=settings_obj),
                status=status.HTTP_200_OK,
            )

        serializer = AppearanceSettingsUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        payload = update_appearance_settings(
            settings_obj=settings_obj,
            data=serializer.validated_data,
        )
        return Response(payload, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "patch"], url_path="me/notifications")
    def notifications(self, request):
        settings_obj = self.get_settings_obj()

        if request.method == "GET":
            return Response(
                build_notification_settings_payload(settings_obj=settings_obj),
                status=status.HTTP_200_OK,
            )

        serializer = NotificationSettingsUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        payload = update_notification_settings(
            settings_obj=settings_obj,
            data=serializer.validated_data,
        )
        return Response(payload, status=status.HTTP_200_OK)
