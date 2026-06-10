from __future__ import annotations

from apps.course.models import Course
from apps.course.selectors.access_selectors import limit_courses_queryset_by_user
from django.db.models import Q, QuerySet


def course_base_queryset() -> QuerySet[Course]:
    """
    Возвращает базовый queryset курсов.
    """

    return Course.objects.select_related(
        "owner_teacher",
        "organization",
        "subject",
        "academic_year",
        "period",
    )


def course_list_queryset(
    *,
    search: str | None = None,
    course_type: str | None = None,
    origin: str | None = None,
    status: str | None = None,
    visibility: str | None = None,
    organization_id: int | None = None,
    subject_id: int | None = None,
    academic_year_id: int | None = None,
    period_id: int | None = None,
    owner_teacher_id: int | None = None,
    is_template: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet[Course]:
    """
    Возвращает список курсов.
    """

    queryset = course_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(subtitle__icontains=search)
            | Q(description__icontains=search)
            | Q(code__icontains=search)
            | Q(slug__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(organization__short_name__icontains=search)
            | Q(organization__code__icontains=search)
            | Q(subject__name__icontains=search)
            | Q(subject__short_name__icontains=search)
            | Q(subject__code__icontains=search)
            | Q(owner_teacher__email__icontains=search)
            | Q(owner_teacher__first_name__icontains=search)
            | Q(owner_teacher__last_name__icontains=search)
        )

    if course_type:
        queryset = queryset.filter(course_type=course_type)

    if origin:
        queryset = queryset.filter(origin=origin)

    if status:
        queryset = queryset.filter(status=status)

    if visibility:
        queryset = queryset.filter(visibility=visibility)

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    if period_id:
        queryset = queryset.filter(period_id=period_id)

    if owner_teacher_id:
        queryset = queryset.filter(owner_teacher_id=owner_teacher_id)

    if is_template is not None:
        queryset = queryset.filter(is_template=is_template)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "organization_id",
        "subject_id",
        "-updated_at",
        "title",
    )


def course_detail_queryset() -> QuerySet[Course]:
    """
    Возвращает queryset курса с деталями.
    """

    return course_base_queryset().prefetch_related(
        "group_accesses",
        "access_rules",
        "sections",
        "lessons",
        "material_links",
        "enrollments",
    )


def get_course_by_id(
    course_id: int,
) -> Course:
    """
    Возвращает курс по идентификатору.
    """

    return course_detail_queryset().get(id=course_id)


def get_course_by_slug(
    slug: str,
) -> Course:
    """
    Возвращает курс по slug.
    """

    return course_detail_queryset().get(slug=slug)


def get_course_by_code(
    code: str,
) -> Course:
    """
    Возвращает курс по коду.
    """

    return course_detail_queryset().get(code=code)


def get_user_available_courses(
    *,
    user,
    search: str | None = None,
    course_type: str | None = None,
    status: str | None = None,
    organization_id: int | None = None,
    subject_id: int | None = None,
    academic_year_id: int | None = None,
    is_active: bool | None = True,
) -> QuerySet[Course]:
    """
    Возвращает курсы, доступные пользователю.
    """

    queryset = course_list_queryset(
        search=search,
        course_type=course_type,
        status=status,
        organization_id=organization_id,
        subject_id=subject_id,
        academic_year_id=academic_year_id,
        is_active=is_active,
    )

    return limit_courses_queryset_by_user(queryset, user)


def get_teacher_courses(
    *,
    teacher_id: int,
    search: str | None = None,
    status: str | None = None,
    is_active: bool | None = None,
) -> QuerySet[Course]:
    """
    Возвращает курсы преподавателя.
    """

    return course_list_queryset(
        search=search,
        status=status,
        owner_teacher_id=teacher_id,
        is_active=is_active,
    )
