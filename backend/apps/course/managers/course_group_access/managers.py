from __future__ import annotations

from apps.course.constants import (
    COURSE_GROUP_VISIBILITY_ARCHIVED,
    COURSE_GROUP_VISIBILITY_HIDDEN,
    COURSE_GROUP_VISIBILITY_VISIBLE,
)
from django.db import models
from django.utils import timezone


class CourseGroupAccessQuerySet(models.QuerySet):
    """
    QuerySet доступов групп к курсу.
    """

    def active(self):
        """
        Возвращает активные доступы.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные доступы.
        """

        return self.filter(is_active=False)

    def visible(self):
        """
        Возвращает видимые доступы.
        """

        return self.filter(visibility=COURSE_GROUP_VISIBILITY_VISIBLE)

    def hidden(self):
        """
        Возвращает скрытые доступы.
        """

        return self.filter(visibility=COURSE_GROUP_VISIBILITY_HIDDEN)

    def archived(self):
        """
        Возвращает архивные доступы.
        """

        return self.filter(visibility=COURSE_GROUP_VISIBILITY_ARCHIVED)

    def for_course(self, course_id: int):
        """
        Фильтрует доступы по курсу.
        """

        return self.filter(course_id=course_id)

    def for_group(self, group_id: int):
        """
        Фильтрует доступы по учебной группе.
        """

        return self.filter(group_id=group_id)

    def for_group_subject(self, group_subject_id: int):
        """
        Фильтрует доступы по предмету группы.
        """

        return self.filter(group_subject_id=group_subject_id)

    def for_teacher_group_subject(self, teacher_group_subject_id: int):
        """
        Фильтрует доступы по назначению преподавателя.
        """

        return self.filter(teacher_group_subject_id=teacher_group_subject_id)

    def auto_enroll(self):
        """
        Возвращает доступы с автозачислением.
        """

        return self.filter(auto_enroll=True)

    def available_on_date(self, reference_date=None):
        """
        Возвращает доступы, действующие на указанную дату.
        """

        current_date = reference_date or timezone.localdate()

        return self.filter(
            models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=current_date),
            models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=current_date),
        )

    def ordered_for_course(self):
        """
        Возвращает доступы в порядке внутри курса.
        """

        return self.order_by(
            "course",
            "group__name",
            "group__code",
        )


class CourseGroupAccessManager(models.Manager.from_queryset(CourseGroupAccessQuerySet)):
    """
    Менеджер доступов групп к курсу.
    """

    use_in_migrations = False
