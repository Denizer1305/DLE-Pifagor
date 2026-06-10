from __future__ import annotations

from apps.testing.constants import (
    TEST_STATUS_CHOICES,
    TEST_VISIBILITY_CHOICES,
    TestStatus,
    TestVisibility,
)
from apps.testing.managers import TestManager
from django.conf import settings
from django.db import models


class Test(models.Model):
    """
    Учебный тест.
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    instructions = models.TextField(
        blank=True,
        verbose_name="Инструкция",
    )

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="tests",
        verbose_name="Курс",
    )
    lesson = models.ForeignKey(
        "course.CourseLesson",
        on_delete=models.SET_NULL,
        related_name="tests",
        null=True,
        blank=True,
        verbose_name="Урок",
    )
    lesson_block = models.ForeignKey(
        "course.CourseLessonBlock",
        on_delete=models.SET_NULL,
        related_name="tests",
        null=True,
        blank=True,
        verbose_name="Блок урока",
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="tests",
        verbose_name="Организация",
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.PROTECT,
        related_name="tests",
        verbose_name="Предмет",
    )
    owner_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_tests",
        verbose_name="Преподаватель-владелец",
    )

    status = models.CharField(
        max_length=32,
        choices=TEST_STATUS_CHOICES,
        default=TestStatus.DRAFT,
        verbose_name="Статус",
    )
    visibility = models.CharField(
        max_length=32,
        choices=TEST_VISIBILITY_CHOICES,
        default=TestVisibility.COURSE,
        verbose_name="Видимость",
    )

    max_attempts = models.PositiveSmallIntegerField(
        default=3,
        verbose_name="Максимум попыток",
    )
    time_limit_minutes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Ограничение времени, минут",
    )
    max_score = models.PositiveIntegerField(
        default=100,
        verbose_name="Максимальный балл",
    )
    passing_score = models.PositiveIntegerField(
        default=50,
        verbose_name="Проходной балл",
    )

    shuffle_questions = models.BooleanField(
        default=False,
        verbose_name="Перемешивать вопросы",
    )
    shuffle_options = models.BooleanField(
        default=False,
        verbose_name="Перемешивать варианты",
    )
    show_correct_answers_after_publish = models.BooleanField(
        default=False,
        verbose_name="Показывать правильные ответы после публикации",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата публикации",
    )
    archived_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата архивирования",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    objects = TestManager()

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = (
            "-updated_at",
            "-id",
        )
        indexes = (
            models.Index(fields=("status",), name="tst_test_status_idx"),
            models.Index(fields=("visibility",), name="tst_test_vis_idx"),
            models.Index(fields=("course",), name="tst_test_course_idx"),
            models.Index(fields=("lesson",), name="tst_test_lesson_idx"),
            models.Index(fields=("organization",), name="tst_test_org_idx"),
            models.Index(fields=("subject",), name="tst_test_subject_idx"),
            models.Index(fields=("owner_teacher",), name="tst_test_owner_idx"),
            models.Index(fields=("is_active",), name="tst_test_active_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает название теста.
        """

        return self.title

    def clean(self) -> None:
        """
        Запускает доменную валидацию теста.
        """

        from apps.testing.validators import validate_test

        validate_test(test=self)
