from __future__ import annotations

from apps.course.constants import (
    COURSE_STATUS_ARCHIVED,
    COURSE_STATUS_DRAFT,
    COURSE_STATUS_PUBLISHED,
)
from django.db import models
from django.utils import timezone


class CourseQuerySet(models.QuerySet):
    """
    QuerySet курсов.
    """

    def active(self):
        """
        Возвращает активные курсы.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные курсы.
        """

        return self.filter(is_active=False)

    def draft(self):
        """
        Возвращает черновики курсов.
        """

        return self.filter(status=COURSE_STATUS_DRAFT)

    def published(self):
        """
        Возвращает опубликованные курсы.
        """

        return self.filter(status=COURSE_STATUS_PUBLISHED)

    def archived(self):
        """
        Возвращает архивные курсы.
        """

        return self.filter(status=COURSE_STATUS_ARCHIVED)

    def templates(self):
        """
        Возвращает шаблоны курсов.
        """

        return self.filter(is_template=True)

    def regular(self):
        """
        Возвращает обычные курсы.
        """

        return self.filter(is_template=False)

    def by_type(self, course_type: str):
        """
        Фильтрует курсы по типу.
        """

        return self.filter(course_type=course_type)

    def by_visibility(self, visibility: str):
        """
        Фильтрует курсы по видимости.
        """

        return self.filter(visibility=visibility)

    def owned_by(self, teacher_id: int):
        """
        Фильтрует курсы по владельцу-преподавателю.
        """

        return self.filter(owner_teacher_id=teacher_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует курсы по организации.
        """

        return self.filter(organization_id=organization_id)

    def for_subject(self, subject_id: int):
        """
        Фильтрует курсы по предмету.
        """

        return self.filter(subject_id=subject_id)

    def for_year(self, academic_year_id: int):
        """
        Фильтрует курсы по учебному году.
        """

        return self.filter(academic_year_id=academic_year_id)

    def for_period(self, period_id: int):
        """
        Фильтрует курсы по учебному периоду.
        """

        return self.filter(period_id=period_id)

    def self_enrollment_allowed(self):
        """
        Возвращает курсы с самостоятельной записью.
        """

        return self.filter(allow_self_enrollment=True)

    def available_on_date(self, reference_date=None):
        """
        Возвращает курсы, доступные на указанную дату.
        """

        current_date = reference_date or timezone.localdate()

        return self.filter(
            models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=current_date),
            models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=current_date),
        )

    def ordered_for_admin(self):
        """
        Возвращает курсы в порядке для админки.
        """

        return self.order_by(
            "organization",
            "subject",
            "-updated_at",
            "title",
        )

    def ordered_for_teacher(self):
        """
        Возвращает курсы в порядке для преподавателя.
        """

        return self.order_by(
            "-is_active",
            "status",
            "title",
        )


class CourseManager(models.Manager.from_queryset(CourseQuerySet)):
    """
    Менеджер курсов.
    """

    use_in_migrations = False
