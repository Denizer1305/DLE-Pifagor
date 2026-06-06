from __future__ import annotations

from apps.organizations.filters import filter_subjects_queryset
from apps.organizations.models import Subject
from apps.organizations.permissions import CanManageSubjects
from apps.organizations.selectors import get_admin_subjects_queryset_for_actor
from apps.organizations.serializers import (
    SubjectDetailSerializer,
    SubjectListSerializer,
    SubjectWriteSerializer,
)
from apps.organizations.services import (
    create_subject,
    deactivate_subject,
    restore_subject,
    update_subject,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminSubjectViewSet(viewsets.ViewSet):
    """
    Административное управление учебными предметами.
    """

    permission_classes = [CanManageSubjects]

    def get_queryset(self):
        """
        Возвращает предметы, доступные текущему пользователю.
        """

        return get_admin_subjects_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> Subject:
        """
        Возвращает предмет из доступного queryset.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список учебных предметов.
        """

        queryset = filter_subjects_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = SubjectListSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку учебного предмета.
        """

        subject = self.get_object()

        serializer = SubjectDetailSerializer(
            subject,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Создаёт учебный предмет.
        """

        serializer = SubjectWriteSerializer(
            data=request.data,
            context={
                "is_create": True,
            },
        )
        serializer.is_valid(raise_exception=True)

        subject = create_subject(
            actor=request.user,
            data=serializer.validated_data,
        )

        output_serializer = SubjectDetailSerializer(
            subject,
            context={
                "request": request,
            },
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        """
        Частично обновляет учебный предмет.
        """

        subject = self.get_object()

        serializer = SubjectWriteSerializer(
            data=request.data,
            partial=True,
            context={
                "is_create": False,
            },
        )
        serializer.is_valid(raise_exception=True)

        subject = update_subject(
            actor=request.user,
            subject=subject,
            data=serializer.validated_data,
        )

        output_serializer = SubjectDetailSerializer(
            subject,
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Деактивирует предмет вместо физического удаления.
        """

        subject = self.get_object()

        subject = deactivate_subject(
            actor=request.user,
            subject=subject,
        )

        serializer = SubjectDetailSerializer(
            subject,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(self, request, pk=None):
        """
        Восстанавливает учебный предмет.
        """

        subject = self.get_object()

        subject = restore_subject(
            actor=request.user,
            subject=subject,
        )

        serializer = SubjectDetailSerializer(
            subject,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)