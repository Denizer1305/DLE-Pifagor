from apps.users.serializers.user_settings_serializers import (
    ChangePasswordSerializer,
    SecuritySettingsUpdateSerializer,
)
from apps.users.services import (
    build_security_sessions_payload,
    build_security_settings_payload,
    update_security_settings,
)
from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserSettingsSecurityMixin:
    @action(detail=False, methods=["get", "patch"], url_path="me/security")
    def security(self, request):
        settings_obj = self.get_settings_obj()

        if request.method == "GET":
            return Response(
                build_security_settings_payload(settings_obj=settings_obj),
                status=status.HTTP_200_OK,
            )

        serializer = SecuritySettingsUpdateSerializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        payload = update_security_settings(
            settings_obj=settings_obj,
            data=serializer.validated_data,
        )
        return Response(payload, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="me/security/change-password",
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data["new_password"])
        request.user.full_clean()
        request.user.save(update_fields=["password", "updated_at"])
        update_session_auth_hash(request, request.user)

        return Response(
            {"detail": "Пароль успешно изменен."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="me/security/sessions")
    def sessions(self, request):
        return Response(
            build_security_sessions_payload(request=request),
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="me/security/sessions/logout-all",
    )
    def logout_all_sessions(self, request):
        return Response(
            {"detail": "Запрос на завершение всех сессий принят."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path=r"me/security/sessions/(?P<session_id>[^/.]+)/logout",
    )
    def logout_session(self, request, session_id=None):
        return Response(
            {
                "detail": "Запрос на завершение сессии принят.",
                "session_id": session_id,
            },
            status=status.HTTP_200_OK,
        )
