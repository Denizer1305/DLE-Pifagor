from __future__ import annotations

from apps.organizations.selectors import (
    get_default_public_organization,
    get_public_organizations_queryset,
    get_user_organization,
)
from apps.organizations.serializers import PublicOrganizationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse


class PublicOrganizationListAPIView(APIView):
    """
    Публичный список образовательных организаций.
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Возвращает публичные организации.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Список организаций.
        """

        queryset = get_public_organizations_queryset()

        serializer = PublicOrganizationSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)


class DefaultPublicOrganizationAPIView(APIView):
    """
    Системная организация по умолчанию.
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Возвращает default_public организацию.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Организация или null.
        """

        organization = get_default_public_organization()

        if not organization:
            return JsonResponse(
                None,
                safe=False,
            )

        serializer = PublicOrganizationSerializer(
            organization,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)


class CurrentUserOrganizationAPIView(APIView):
    """
    Организация текущего пользователя.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Возвращает организацию текущего пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Организация или null.
        """

        organization = get_user_organization(request.user)

        if not organization:
            return JsonResponse(
                None,
                safe=False,
            )

        serializer = PublicOrganizationSerializer(
            organization,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
