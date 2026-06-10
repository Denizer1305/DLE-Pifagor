from __future__ import annotations

from apps.education.filters import LearnerGroupEnrollmentFilter
from apps.education.permissions import LearnerGroupEnrollmentPermission
from apps.education.selectors import (
    get_user_available_group_ids,
    learner_group_enrollment_detail_queryset,
    user_is_global_admin,
    user_is_learner,
    user_is_organization_admin,
    user_is_teacher,
)
from apps.education.serializers import (
    LearnerGroupEnrollmentCompleteSerializer,
    LearnerGroupEnrollmentReadSerializer,
    LearnerGroupEnrollmentWriteSerializer,
)
from apps.education.services import (
    archive_learner_group_enrollment,
    complete_learner_group_enrollment,
    set_primary_learner_group_enrollment,
)
from apps.education.tasks import assign_missing_journal_numbers
from apps.education.views.shared import EducationReadWriteViewSetMixin
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response


class AssignJournalNumbersSerializer(serializers.Serializer):
    """
    Сериализатор назначения номеров в журнале.
    """

    group_id = serializers.IntegerField(min_value=1)
    academic_year_id = serializers.IntegerField(min_value=1)
    start_number = serializers.IntegerField(
        min_value=1,
        default=1,
        required=False,
    )


class LearnerGroupEnrollmentArchiveSerializer(serializers.Serializer):
    """
    Сериализатор архивирования академического зачисления.
    """

    completion_date = serializers.DateField(required=False)


class LearnerGroupEnrollmentViewSet(EducationReadWriteViewSetMixin):
    """
    Административный API академических зачислений обучающихся.
    """

    permission_classes = (LearnerGroupEnrollmentPermission,)
    filterset_class = LearnerGroupEnrollmentFilter
    read_serializer_class = LearnerGroupEnrollmentReadSerializer
    write_serializer_class = LearnerGroupEnrollmentWriteSerializer

    def get_queryset(self):
        """
        Возвращает queryset академических зачислений.
        """

        queryset = learner_group_enrollment_detail_queryset()
        user = self.request.user

        if user_is_global_admin(user):
            return queryset

        if user_is_organization_admin(user):
            group_ids = get_user_available_group_ids(user)

            return queryset.filter(group_id__in=group_ids)

        if user_is_teacher(user):
            group_ids = get_user_available_group_ids(user)

            return queryset.filter(group_id__in=group_ids)

        if user_is_learner(user):
            return queryset.filter(learner=user)

        return queryset.none()

    @action(
        detail=True,
        methods=["post"],
        url_path="set-primary",
    )
    def set_primary(self, request, pk=None) -> Response:
        """
        Делает зачисление основным для обучающегося.
        """

        enrollment = self.get_object()
        enrollment = set_primary_learner_group_enrollment(
            enrollment=enrollment,
        )

        return self.build_read_response(enrollment)

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None) -> Response:
        """
        Завершает академическое зачисление.
        """

        enrollment = self.get_object()

        serializer = LearnerGroupEnrollmentCompleteSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        enrollment = complete_learner_group_enrollment(
            enrollment=enrollment,
            completion_date=serializer.validated_data["completion_date"],
            status=serializer.validated_data["status"],
        )

        return self.build_read_response(enrollment)

    @action(
        detail=True,
        methods=["post"],
        url_path="archive",
    )
    def archive(self, request, pk=None) -> Response:
        """
        Архивирует академическое зачисление.
        """

        enrollment = self.get_object()

        serializer = LearnerGroupEnrollmentArchiveSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        completion_date = serializer.validated_data.get(
            "completion_date",
            timezone.localdate(),
        )

        enrollment = archive_learner_group_enrollment(
            enrollment=enrollment,
            completion_date=completion_date,
        )

        return self.build_read_response(enrollment)

    @action(
        detail=False,
        methods=["post"],
        url_path="assign-journal-numbers",
    )
    def assign_journal_numbers(self, request) -> Response:
        """
        Назначает недостающие номера в журнале.
        """

        serializer = AssignJournalNumbersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = assign_missing_journal_numbers(
            group_id=serializer.validated_data["group_id"],
            academic_year_id=serializer.validated_data["academic_year_id"],
            start_number=serializer.validated_data["start_number"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
