from __future__ import annotations

from apps.course.models import Course, CourseLesson, CourseSection
from django.db import transaction
from django.db.models import Sum


@transaction.atomic
def recalculate_course_section_hours(
    *,
    section: CourseSection,
) -> CourseSection:
    """
    Пересчитывает плановые часы раздела по урокам.
    """

    planned_hours = (
        CourseLesson.objects.filter(
            section=section,
            is_active=True,
        ).aggregate(
            total=Sum("planned_hours")
        )["total"]
        or 0
    )

    section.planned_hours = planned_hours
    section.full_clean()
    section.save(
        update_fields=[
            "planned_hours",
            "updated_at",
        ],
    )

    return section


@transaction.atomic
def recalculate_course_sections_hours(
    *,
    course: Course,
) -> dict[str, int]:
    """
    Пересчитывает часы всех разделов курса.
    """

    updated_count = 0

    for section in course.sections.all():
        recalculate_course_section_hours(section=section)
        updated_count += 1

    return {
        "updated": updated_count,
    }


def collect_course_structure_stats(
    *,
    course: Course,
) -> dict[str, int]:
    """
    Собирает статистику структуры курса.
    """

    lessons = CourseLesson.objects.filter(course=course)

    return {
        "sections_count": course.sections.count(),
        "lessons_count": lessons.count(),
        "published_lessons_count": lessons.filter(is_published=True).count(),
        "blocks_count": course.lessons.filter(blocks__isnull=False).count(),
        "material_links_count": course.material_links.count(),
        "planned_hours": lessons.aggregate(total=Sum("planned_hours"))["total"] or 0,
    }
