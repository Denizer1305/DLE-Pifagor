from __future__ import annotations

from apps.course.models import CourseEnrollment, CourseProgress, LessonProgress
from apps.course.selectors import get_course_enrollment_by_id
from django.db import transaction


@transaction.atomic
def ensure_course_progress(
    *,
    enrollment: CourseEnrollment,
) -> CourseProgress:
    """
    Гарантирует наличие прогресса курса для записи на курс.
    """

    defaults = _build_model_kwargs(
        CourseProgress,
        progress_percent=getattr(enrollment, "progress_percent", 0),
        total_lessons_count=0,
        completed_lessons_count=0,
        last_lesson=None,
        last_activity_at=getattr(enrollment, "last_activity_at", None),
    )

    progress, _ = CourseProgress.objects.get_or_create(
        enrollment=enrollment,
        defaults=defaults,
    )

    return progress


@transaction.atomic
def ensure_course_progress_by_enrollment_id(
    *,
    enrollment_id: int,
) -> CourseProgress:
    """
    Гарантирует наличие прогресса курса по идентификатору записи.
    """

    enrollment = get_course_enrollment_by_id(enrollment_id)

    return ensure_course_progress(enrollment=enrollment)


@transaction.atomic
def ensure_lesson_progress(
    *,
    enrollment: CourseEnrollment,
    lesson,
) -> LessonProgress:
    """
    Гарантирует наличие прогресса конкретного урока.
    """

    course_progress = ensure_course_progress(enrollment=enrollment)

    defaults = _build_model_kwargs(
        LessonProgress,
        course_progress=course_progress,
        status=_get_lesson_status_value("NOT_STARTED", "not_started"),
        progress_percent=0,
        started_at=None,
        completed_at=None,
        last_activity_at=None,
    )

    lesson_progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson,
        defaults=defaults,
    )

    if (
        _model_has_field(LessonProgress, "course_progress")
        and lesson_progress.course_progress_id != course_progress.id
    ):
        lesson_progress.course_progress = course_progress
        _save_model_fields(
            lesson_progress,
            [
                "course_progress",
                "updated_at",
            ],
        )

    return lesson_progress


@transaction.atomic
def ensure_lesson_progresses_for_enrollment(
    *,
    enrollment: CourseEnrollment,
) -> dict[str, int]:
    """
    Создаёт недостающие записи прогресса по всем активным урокам курса.
    """

    lessons_queryset = enrollment.course.lessons.filter(is_active=True)

    if _model_has_field(lessons_queryset.model, "is_published"):
        lessons_queryset = lessons_queryset.filter(is_published=True)

    created_count = 0
    existing_count = 0

    for lesson in lessons_queryset:
        _, created = _ensure_lesson_progress_with_created_flag(
            enrollment=enrollment,
            lesson=lesson,
        )

        if created:
            created_count += 1
        else:
            existing_count += 1

    return {
        "created": created_count,
        "existing": existing_count,
    }


def _ensure_lesson_progress_with_created_flag(
    *,
    enrollment: CourseEnrollment,
    lesson,
) -> tuple[LessonProgress, bool]:
    """
    Возвращает прогресс урока и признак создания.
    """

    course_progress = ensure_course_progress(enrollment=enrollment)

    defaults = _build_model_kwargs(
        LessonProgress,
        course_progress=course_progress,
        status=_get_lesson_status_value("NOT_STARTED", "not_started"),
        progress_percent=0,
    )

    return LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson,
        defaults=defaults,
    )


def _get_lesson_status_value(
    name: str,
    default: str,
) -> str:
    """
    Возвращает значение статуса урока с защитой от отличий enum.
    """

    status_choices = getattr(LessonProgress, "StatusChoices", None)

    if status_choices is None:
        return default

    return getattr(status_choices, name, default)


def _build_model_kwargs(
    model,
    **kwargs,
) -> dict:
    """
    Оставляет только реально существующие поля модели.
    """

    field_names = {field.name for field in model._meta.fields}

    return {key: value for key, value in kwargs.items() if key in field_names}


def _model_has_field(
    model,
    field_name: str,
) -> bool:
    """
    Проверяет наличие поля в модели.
    """

    return any(field.name == field_name for field in model._meta.fields)


def _save_model_fields(
    instance,
    field_names: list[str],
) -> None:
    """
    Сохраняет только существующие поля модели.
    """

    model = type(instance)

    existing_fields = [
        field_name for field_name in field_names if _model_has_field(model, field_name)
    ]

    if existing_fields:
        instance.save(update_fields=existing_fields)
        return

    instance.save()
