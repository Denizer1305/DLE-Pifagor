from __future__ import annotations

from apps.organizations.selectors import (
    get_public_teacher_subjects_queryset,
    get_public_teachers_queryset,
    resolve_public_teachers_organization,
)
from apps.organizations.serializers import (
    PublicOrganizationSerializer,
    PublicSubjectSerializer,
    PublicTeacherSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PublicTeachersPageAPIView(APIView):
    """
    Данные для публичной страницы преподавателей.

    Если пользователь авторизован, берётся его организация.
    Если пользователь не авторизован, берётся default_public организация.
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Возвращает организацию, предметы и преподавателей.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Данные страницы преподавателей.
        """

        user = request.user if request.user.is_authenticated else None
        organization = resolve_public_teachers_organization(user)

        if not organization:
            return Response(
                {
                    "organization": None,
                    "subjects": [],
                    "teachers": [],
                    "meta": {
                        "teachers_count": 0,
                        "subjects_count": 0,
                        "is_fallback": True,
                        "message": (
                            "Организация для публичной страницы преподавателей "
                            "пока не настроена."
                        ),
                    },
                }
            )

        search = request.query_params.get("search", "")
        subject = request.query_params.get("subject", "")
        position = request.query_params.get("position", "")

        teachers_queryset = get_public_teachers_queryset(
            organization=organization,
            search=search,
            subject=subject,
            position=position,
        )
        subjects_queryset = get_public_teacher_subjects_queryset(organization)

        organization_data = PublicOrganizationSerializer(
            organization,
            context={
                "request": request,
            },
        ).data

        subjects_data = PublicSubjectSerializer(
            subjects_queryset,
            many=True,
            context={
                "request": request,
            },
        ).data

        teachers_data = PublicTeacherSerializer(
            teachers_queryset,
            many=True,
            context={
                "request": request,
            },
        ).data

        return Response(
            {
                "organization": organization_data,
                "subjects": subjects_data,
                "teachers": teachers_data,
                "meta": {
                    "teachers_count": teachers_queryset.count(),
                    "subjects_count": subjects_queryset.count(),
                    "is_fallback": user is None,
                    "search": search,
                    "subject": subject,
                    "position": position,
                },
            }
        )