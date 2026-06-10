from __future__ import annotations

from apps.testing.constants import TestStatus, TestVisibility
from django.db import models


class TestQuerySet(models.QuerySet):
    """
    QuerySet тестов.
    """

    def active(self):
        """
        Возвращает активные тесты.
        """

        return self.filter(is_active=True)

    def drafts(self):
        """
        Возвращает черновики тестов.
        """

        return self.filter(status=TestStatus.DRAFT)

    def published(self):
        """
        Возвращает опубликованные тесты.
        """

        return self.filter(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )

    def archived(self):
        """
        Возвращает архивные тесты.
        """

        return self.filter(status=TestStatus.ARCHIVED)

    def visible_for_course(self):
        """
        Возвращает тесты, видимые участникам курса.
        """

        return self.filter(
            visibility=TestVisibility.COURSE,
            status=TestStatus.PUBLISHED,
            is_active=True,
        )

    def for_course(self, course_id: int):
        """
        Фильтрует тесты по курсу.
        """

        return self.filter(course_id=course_id)

    def for_lesson(self, lesson_id: int):
        """
        Фильтрует тесты по уроку.
        """

        return self.filter(lesson_id=lesson_id)

    def for_lesson_block(self, lesson_block_id: int):
        """
        Фильтрует тесты по блоку урока.
        """

        return self.filter(lesson_block_id=lesson_block_id)

    def for_organization(self, organization_id: int):
        """
        Фильтрует тесты по организации.
        """

        return self.filter(organization_id=organization_id)

    def for_subject(self, subject_id: int):
        """
        Фильтрует тесты по предмету.
        """

        return self.filter(subject_id=subject_id)

    def owned_by(self, teacher_id: int):
        """
        Фильтрует тесты по преподавателю-владельцу.
        """

        return self.filter(owner_teacher_id=teacher_id)
