from __future__ import annotations

from apps.course.models import (
    Course,
    CourseLesson,
    CourseLessonBlock,
    CourseMaterialLink,
    CourseSection,
)
from apps.course.selectors import get_course_by_id
from django.db import transaction
from django.utils.text import slugify


@transaction.atomic
def duplicate_course(
    *,
    course: Course,
    owner_teacher=None,
    title: str | None = None,
    code: str | None = None,
    slug: str | None = None,
    copy_material_links: bool = True,
) -> Course:
    """
    Создаёт копию курса вместе со структурой разделов, уроков и блоков.
    """

    new_course = Course.objects.create(
        code=code or f"{course.code}_copy",
        slug=slug or _build_copy_slug(course),
        title=title or f"{course.title} — копия",
        subtitle=course.subtitle,
        description=course.description,
        course_type=course.course_type,
        origin=Course.OriginChoices.TEMPLATE,
        status=Course.StatusChoices.DRAFT,
        visibility=Course.VisibilityChoices.PRIVATE,
        level=course.level,
        language=course.language,
        owner_teacher=owner_teacher or course.owner_teacher,
        organization=course.organization,
        subject=course.subject,
        academic_year=course.academic_year,
        period=course.period,
        is_template=False,
        is_active=True,
        allow_self_enrollment=False,
        starts_at=course.starts_at,
        ends_at=course.ends_at,
    )

    section_map: dict[int, CourseSection] = {}
    lesson_map: dict[int, CourseLesson] = {}

    for section in course.sections.order_by("order", "id"):
        new_section = CourseSection.objects.create(
            course=new_course,
            title=section.title,
            description=section.description,
            section_number=section.section_number,
            order=section.order,
            planned_hours=section.planned_hours,
            is_required=section.is_required,
            is_published=False,
            is_active=section.is_active,
        )
        section_map[section.id] = new_section

    for lesson in course.lessons.order_by("section__order", "order", "id"):
        new_lesson = CourseLesson.objects.create(
            course=new_course,
            section=section_map.get(lesson.section_id),
            lesson_number=lesson.lesson_number,
            lesson_type=lesson.lesson_type,
            title=lesson.title,
            short_content=lesson.short_content,
            planned_hours=lesson.planned_hours,
            theory_hours=lesson.theory_hours,
            practice_hours=lesson.practice_hours,
            lab_hours=lesson.lab_hours,
            self_study_hours=lesson.self_study_hours,
            visual_aids=lesson.visual_aids,
            literature=lesson.literature,
            independent_work=lesson.independent_work,
            notes=lesson.notes,
            order=lesson.order,
            available_from=lesson.available_from,
            is_required=lesson.is_required,
            is_preview=lesson.is_preview,
            is_published=False,
            is_active=lesson.is_active,
        )
        lesson_map[lesson.id] = new_lesson

    for block in CourseLessonBlock.objects.filter(
        lesson__course=course,
    ).order_by("lesson_id", "order", "id"):
        CourseLessonBlock.objects.create(
            lesson=lesson_map[block.lesson_id],
            block_type=block.block_type,
            title=block.title,
            content=block.content,
            external_url=block.external_url,
            material=block.material,
            order=block.order,
            is_visible=block.is_visible,
        )

    if copy_material_links:
        for link in CourseMaterialLink.objects.filter(course=course).order_by(
            "order",
            "id",
        ):
            CourseMaterialLink.objects.create(
                course=new_course,
                section=section_map.get(link.section_id),
                lesson=lesson_map.get(link.lesson_id),
                material=link.material,
                placement=link.placement,
                order=link.order,
                is_required=link.is_required,
                is_visible=link.is_visible,
                notes=link.notes,
            )

    return new_course


@transaction.atomic
def duplicate_course_by_id(
    *,
    course_id: int,
    owner_teacher=None,
    title: str | None = None,
    code: str | None = None,
    slug: str | None = None,
    copy_material_links: bool = True,
) -> Course:
    """
    Создаёт копию курса по идентификатору.
    """

    course = get_course_by_id(course_id)

    return duplicate_course(
        course=course,
        owner_teacher=owner_teacher,
        title=title,
        code=code,
        slug=slug,
        copy_material_links=copy_material_links,
    )


def _build_copy_slug(course: Course) -> str:
    """
    Формирует slug копии курса.
    """

    base_slug = course.slug or slugify(course.title)

    return f"{base_slug}-copy"
