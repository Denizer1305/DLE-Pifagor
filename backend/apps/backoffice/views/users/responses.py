from __future__ import annotations

from apps.backoffice.serializers.users import BackofficeUserDetailSerializer
from rest_framework.response import Response


class BackofficeUserResponseMixin:
    """
    Mixin ответов для backoffice user viewset.
    """

    def get_fresh_backoffice_user(self, user):
        """
        Возвращает свежую карточку пользователя из queryset viewset.

        Нужно после изменения ролей, статуса или удаления, чтобы serializer
        получил актуальные select_related/prefetch_related данные.
        """

        return self.get_queryset().get(id=user.id)

    def serialize_backoffice_user(self, user) -> dict:
        """
        Возвращает детальную карточку пользователя.
        """

        return BackofficeUserDetailSerializer(
            user,
            context=self.get_serializer_context(),
        ).data

    def respond_with_backoffice_user(
        self,
        user,
        *,
        status_code: int = 200,
        refresh: bool = True,
    ):
        """
        Возвращает Response с детальной карточкой пользователя.
        """

        response_user = self.get_fresh_backoffice_user(user) if refresh else user

        return Response(
            self.serialize_backoffice_user(response_user),
            status=status_code,
        )
