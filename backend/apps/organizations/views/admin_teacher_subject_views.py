from __future__ import annotations

from apps.organizations.filters import filter_teacher_subjects_queryset
from apps.organizations.models import TeacherSubject
from apps.organizations.permissions import CanManageTeacherSubjects
from apps.organizations.selectors import (
    get_admin_teacher_subjects_queryset_for_actor,
)
from apps.organizations.serializers import (
    TeacherSubjectDetailSerializer,
    TeacherSubjectListSerializer,
    TeacherSubjectWriteSerializer,
)
from apps.organizations.services import (
    assign_subject_to_teacher,
    deactivate_teacher_subject,
    restore_teacher_subject,
    set_primary_teacher_subject,
    update_teacher_subject,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AdminTeacherSubjectViewSet(viewsets.ViewSet):
    """
    Административное управление предметами преподавателей.
    """

    permission_classes = [CanManageTeacherSubjects]

    def get_queryset(self):
        """
        Возвращает предметы преподавателей, доступные текущему пользователю.
        """

        return get_admin_teacher_subjects_queryset_for_actor(
            actor=self.request.user,
        )

    def get_object(self) -> TeacherSubject:
        """
        Возвращает связь преподавателя с предметом из доступного queryset.
        """

        return self.get_queryset().get(pk=self.kwargs["pk"])

    def list(self, request):
        """
        Возвращает список предметов преподавателей.
        """

        queryset = filter_teacher_subjects_queryset(
            queryset=self.get_queryset(),
            params=request.query_params,
        )

        serializer = TeacherSubjectListSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную карточку предмета преподавателя.
        """

        teacher_subject = self.get_object()

        serializer = TeacherSubjectDetailSerializer(
            teacher_subject,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def create(self, request):
        """
        Назначает предмет преподавателю.
        """

        serializer = TeacherSubjectWriteSerializer(
            data=request.data,
            context={
                "is_create": True,
            },
        )
        serializer.is_valid(raise_exception=True)

        teacher_subject = assign_subject_to_teacher(
            actor=request.user,
            teacher=serializer.validated_data["teacher"],
            subject=serializer.validated_data["subject"],
            data=serializer.validated_data,
        )

        output_serializer = TeacherSubjectDetailSerializer(
            teacher_subject,
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
        Частично обновляет предмет преподавателя.
        """

        teacher_subject = self.get_object()

        serializer = TeacherSubjectWriteSerializer(
            data=request.data,
            partial=True,
            context={
                "is_create": False,
            },
        )
        serializer.is_valid(raise_exception=True)

        teacher_subject = update_teacher_subject(
            actor=request.user,
            teacher_subject=teacher_subject,
            data=serializer.validated_data,
        )

        output_serializer = TeacherSubjectDetailSerializer(
            teacher_subject,
            context={
                "request": request,
            },
        )

        return Response(output_serializer.data)

    def destroy(self, request, pk=None):
        """
        Деактивирует предмет преподавателя.
        """

        teacher_subject = self.get_object()

        teacher_subject = deactivate_teacher_subject(
            actor=request.user,
            teacher_subject=teacher_subject,
        )

        serializer = TeacherSubjectDetailSerializer(
            teacher_subject,
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
        Восстанавливает предмет преподавателя.
        """

        teacher_subject = self.get_object()

        teacher_subject = restore_teacher_subject(
            actor=request.user,
            teacher_subject=teacher_subject,
        )

        serializer = TeacherSubjectDetailSerializer(
            teacher_subject,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="set-primary",
    )
    def set_primary(self, request, pk=None):
        """
        Делает предмет основным для преподавателя.
        """

        teacher_subject = self.get_object()

        teacher_subject = set_primary_teacher_subject(
            actor=request.user,
            teacher_subject=teacher_subject,
        )

        serializer = TeacherSubjectDetailSerializer(
            teacher_subject,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)