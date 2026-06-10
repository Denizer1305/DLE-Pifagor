from __future__ import annotations

from apps.course.constants import (
    COURSE_ACCESS_TYPE_INVITE_CODE,
    COURSE_ACCESS_TYPE_LEARNER,
    COURSE_ACCESS_TYPE_ORGANIZATION,
    COURSE_ACCESS_TYPE_PUBLIC_LINK,
)
from django.db import models
from django.utils import timezone


class CourseAccessRuleQuerySet(models.QuerySet):
    """
    QuerySet правил доступа к курсу.
    """

    def active(self):
        """
        Возвращает активные правила.
        """

        return self.filter(is_active=True)

    def inactive(self):
        """
        Возвращает неактивные правила.
        """

        return self.filter(is_active=False)

    def for_course(self, course_id: int):
        """
        Фильтрует правила по курсу.
        """

        return self.filter(course_id=course_id)

    def for_learner(self, learner_id: int):
        """
        Фильтрует персональные правила по обучающемуся.
        """

        return self.filter(
            access_type=COURSE_ACCESS_TYPE_LEARNER,
            learner_id=learner_id,
        )

    def for_organization(self, organization_id: int):
        """
        Фильтрует правила по организации.
        """

        return self.filter(
            access_type=COURSE_ACCESS_TYPE_ORGANIZATION,
            organization_id=organization_id,
        )

    def public_links(self):
        """
        Возвращает правила публичных ссылок.
        """

        return self.filter(access_type=COURSE_ACCESS_TYPE_PUBLIC_LINK)

    def invite_codes(self):
        """
        Возвращает правила кодов приглашения.
        """

        return self.filter(access_type=COURSE_ACCESS_TYPE_INVITE_CODE)

    def auto_enroll(self):
        """
        Возвращает правила с автозачислением.
        """

        return self.filter(auto_enroll=True)

    def available_on_date(self, reference_date=None):
        """
        Возвращает правила, действующие на указанную дату.
        """

        current_date = reference_date or timezone.localdate()

        return self.filter(
            models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=current_date),
            models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=current_date),
        )

    def ordered_for_course(self):
        """
        Возвращает правила в порядке курса.
        """

        return self.order_by(
            "course",
            "access_type",
            "id",
        )


class CourseAccessRuleManager(models.Manager.from_queryset(CourseAccessRuleQuerySet)):
    """
    Менеджер правил доступа к курсу.
    """

    use_in_migrations = False
