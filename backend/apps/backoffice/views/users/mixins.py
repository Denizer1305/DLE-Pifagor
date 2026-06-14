from __future__ import annotations

from apps.backoffice.serializers.users import BackofficeUserDetailSerializer
from rest_framework.response import Response


class BackofficeUserResponseMixin:
    """
    Mixin ответов для backoffice user viewset.
    """

    def get_response_context(self) -> dict:
        """
        Возвращает serializer context для response-сериализаторов.
        """

        return self.get_serializer_context()

    def serialize_backoffice_user(self, user) -> dict:
        """
        Возвращает детальное представление пользователя.
        """

        return BackofficeUserDetailSerializer(
            user,
            context=self.get_response_context(),
        ).data

    def respond_with_backoffice_user(self, user, *, status_code: int = 200):
        """
        Возвращает Response с детальной карточкой пользователя.
        """

        return Response(
            self.serialize_backoffice_user(user),
            status=status_code,
        )

    def get_action_reason(self, serializer) -> str:
        """
        Возвращает причину административного действия.
        """

        return serializer.validated_data.get("reason", "") or ""

    def get_action_expected_updated_at(self, serializer):
        """
        Возвращает expected_updated_at из action serializer.
        """

        return serializer.validated_data.get("expected_updated_at")
