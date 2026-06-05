from apps.users.serializers.user_settings_serializers import (
    PrivacySettingsUpdateSerializer,
    RoleSettingsUpdateSerializer,
)
from apps.users.services import (
    build_privacy_settings_payload,
    build_role_settings_payload,
    update_privacy_settings,
    update_role_settings,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserSettingsAccessMixin:
    @action(detail=False, methods=["get", "patch"], url_path="me/privacy")
    def privacy(self, request):
        settings_obj = self.get_settings_obj()

        if request.method == "GET":
            return Response(
                build_privacy_settings_payload(settings_obj=settings_obj),
                status=status.HTTP_200_OK,
            )

        serializer = PrivacySettingsUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        payload = update_privacy_settings(
            settings_obj=settings_obj,
            data=serializer.validated_data,
        )
        return Response(payload, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "patch"], url_path="me/roles")
    def roles(self, request):
        settings_obj = self.get_settings_obj()

        if request.method == "GET":
            return Response(
                build_role_settings_payload(settings_obj=settings_obj),
                status=status.HTTP_200_OK,
            )

        serializer = RoleSettingsUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        payload = update_role_settings(
            settings_obj=settings_obj,
            data=serializer.validated_data,
        )
        return Response(payload, status=status.HTTP_200_OK)
