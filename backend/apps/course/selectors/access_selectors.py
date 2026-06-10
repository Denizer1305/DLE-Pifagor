from __future__ import annotations

from apps.course.models import Course
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

User = get_user_model()

GLOBAL_COURSE_ADMIN_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
    }
)

ORGANIZATION_COURSE_ADMIN_ROLE_CODES = frozenset(
    {
        "org_admin",
        "director",
        "head_of_department",
    }
)

COURSE_TEACHER_ROLE_CODES = frozenset(
    {
        "teacher",
    }
)

COURSE_LEARNER_ROLE_CODES = frozenset(
    {
        "learner",
    }
)

COURSE_EDITOR_ROLE_CODES = frozenset(
    {
        "superadmin",
        "platform_admin",
        "admin",
        "org_admin",
        "director",
        "head_of_department",
        "teacher",
    }
)


def user_is_authenticated(user: User) -> bool:
    """
    Проверяет, авторизован ли пользователь.
    """

    return bool(user and user.is_authenticated)


def get_user_role_codes(user: User) -> set[str]:
    """
    Возвращает коды ролей пользователя.
    """

    if not user_is_authenticated(user):
        return set()

    role_codes: set[str] = set()

    direct_role = getattr(user, "role", None)
    direct_role_code = getattr(direct_role, "code", None)

    if direct_role_code:
        role_codes.add(str(direct_role_code))

    user_roles = getattr(user, "user_roles", None)

    if user_roles is not None:
        for user_role in user_roles.all():
            status = str(getattr(user_role, "status", "active"))

            if status != "active":
                continue

            role = getattr(user_role, "role", None)
            role_code = getattr(role, "code", None)

            if role_code:
                role_codes.add(str(role_code))

    roles = getattr(user, "roles", None)

    if roles is not None:
        try:
            for role in roles.all():
                role_code = getattr(role, "code", None)

                if role_code:
                    role_codes.add(str(role_code))
        except TypeError:
            pass

    if getattr(user, "is_superuser", False):
        role_codes.add("superadmin")

    if getattr(user, "is_staff", False):
        role_codes.add("admin")

    return role_codes


def user_has_any_role(
    user: User,
    role_codes: frozenset[str] | set[str],
) -> bool:
    """
    Проверяет наличие хотя бы одной роли.
    """

    return bool(get_user_role_codes(user).intersection(role_codes))


def user_is_global_course_admin(user: User) -> bool:
    """
    Проверяет глобального администратора курсов.
    """

    return user_has_any_role(user, GLOBAL_COURSE_ADMIN_ROLE_CODES)


def user_is_organization_course_admin(user: User) -> bool:
    """
    Проверяет администратора организации.
    """

    return user_has_any_role(user, ORGANIZATION_COURSE_ADMIN_ROLE_CODES)


def user_is_course_teacher(user: User) -> bool:
    """
    Проверяет преподавателя.
    """

    return user_has_any_role(user, COURSE_TEACHER_ROLE_CODES)


def user_is_course_learner(user: User) -> bool:
    """
    Проверяет обучающегося.
    """

    return user_has_any_role(user, COURSE_LEARNER_ROLE_CODES)


def user_can_edit_courses(user: User) -> bool:
    """
    Проверяет базовое право редактирования курсов.
    """

    return user_has_any_role(user, COURSE_EDITOR_ROLE_CODES)


def get_user_available_organization_ids(user: User) -> set[int]:
    """
    Возвращает организации, доступные пользователю.
    """

    if not user_is_authenticated(user):
        return set()

    Organization = _get_model_or_none("organizations", "Organization")

    if Organization is None:
        return set()

    if user_is_global_course_admin(user):
        return set(Organization.objects.values_list("id", flat=True))

    organization_ids: set[int] = set()

    direct_organization_id = getattr(user, "organization_id", None)

    if direct_organization_id:
        organization_ids.add(int(direct_organization_id))

    _collect_organizations_from_user_roles(
        user=user,
        organization_ids=organization_ids,
    )
    _collect_teacher_organizations(
        user=user,
        organization_ids=organization_ids,
    )
    _collect_learner_organizations(
        user=user,
        organization_ids=organization_ids,
    )
    _collect_curator_organizations(
        user=user,
        organization_ids=organization_ids,
    )

    return organization_ids


def user_can_access_organization(
    *,
    user: User,
    organization_id: int | None,
) -> bool:
    """
    Проверяет доступ пользователя к организации.
    """

    if not organization_id:
        return False

    if user_is_global_course_admin(user):
        return True

    return organization_id in get_user_available_organization_ids(user)


def limit_queryset_by_user_organizations(
    queryset: QuerySet,
    user: User,
    *,
    organization_field: str = "organization_id",
    include_global: bool = False,
) -> QuerySet:
    """
    Ограничивает queryset организациями пользователя.
    """

    if not user_is_authenticated(user):
        return queryset.none()

    if user_is_global_course_admin(user):
        return queryset

    organization_ids = get_user_available_organization_ids(user)

    query = Q(**{f"{organization_field}__in": organization_ids})

    if include_global:
        query |= Q(**{f"{organization_field}__isnull": True})

    return queryset.filter(query)


def user_can_read_course(
    *,
    user: User,
    course: Course,
) -> bool:
    """
    Проверяет право чтения курса.
    """

    if not user_is_authenticated(user):
        return False

    if user_is_global_course_admin(user):
        return True

    if course.owner_teacher_id == getattr(user, "id", None):
        return True

    if course.organization_id:
        if user_can_access_organization(
            user=user,
            organization_id=course.organization_id,
        ):
            return True

    return _user_has_course_enrollment(
        user=user,
        course_id=course.id,
    )


def user_can_manage_course(
    *,
    user: User,
    course: Course,
) -> bool:
    """
    Проверяет право управления курсом.
    """

    if not user_is_authenticated(user):
        return False

    if user_is_global_course_admin(user):
        return True

    if course.owner_teacher_id == getattr(user, "id", None):
        return True

    if course.organization_id:
        return bool(
            user_is_organization_course_admin(user)
            and user_can_access_organization(
                user=user,
                organization_id=course.organization_id,
            )
        )

    return False


def limit_courses_queryset_by_user(
    queryset: QuerySet[Course],
    user: User,
) -> QuerySet[Course]:
    """
    Ограничивает курсы по доступу пользователя.
    """

    if not user_is_authenticated(user):
        return queryset.none()

    if user_is_global_course_admin(user):
        return queryset

    organization_ids = get_user_available_organization_ids(user)
    enrolled_course_ids = _get_user_enrolled_course_ids(user)

    return queryset.filter(
        Q(owner_teacher=user)
        | Q(organization_id__in=organization_ids)
        | Q(id__in=enrolled_course_ids)
    ).distinct()


def _user_has_course_enrollment(
    *,
    user: User,
    course_id: int,
) -> bool:
    """
    Проверяет запись пользователя на курс.
    """

    CourseEnrollment = _get_model_or_none("course", "CourseEnrollment")

    if CourseEnrollment is None:
        return False

    return CourseEnrollment.objects.filter(
        course_id=course_id,
        learner=user,
    ).exists()


def _get_user_enrolled_course_ids(user: User) -> set[int]:
    """
    Возвращает курсы, на которые записан пользователь.
    """

    CourseEnrollment = _get_model_or_none("course", "CourseEnrollment")

    if CourseEnrollment is None:
        return set()

    return set(
        CourseEnrollment.objects.filter(learner=user).values_list(
            "course_id",
            flat=True,
        )
    )


def _collect_organizations_from_user_roles(
    *,
    user: User,
    organization_ids: set[int],
) -> None:
    """
    Собирает организации из user_roles.
    """

    user_roles = getattr(user, "user_roles", None)

    if user_roles is None:
        return

    for user_role in user_roles.all():
        status = str(getattr(user_role, "status", "active"))

        if status != "active":
            continue

        organization_id = getattr(user_role, "organization_id", None)

        if organization_id:
            organization_ids.add(int(organization_id))

        department = getattr(user_role, "department", None)
        department_organization_id = getattr(
            department,
            "organization_id",
            None,
        )

        if department_organization_id:
            organization_ids.add(int(department_organization_id))


def _collect_teacher_organizations(
    *,
    user: User,
    organization_ids: set[int],
) -> None:
    """
    Собирает организации преподавателя.
    """

    TeacherOrganization = _get_model_or_none(
        "organizations",
        "TeacherOrganization",
    )

    if TeacherOrganization is None:
        return

    teacher_field = _get_first_existing_field_name(
        TeacherOrganization,
        [
            "teacher",
            "user",
            "employee",
        ],
    )

    if teacher_field is None:
        return

    queryset = TeacherOrganization.objects.filter(**{teacher_field: user})

    if _model_has_field(TeacherOrganization, "is_active"):
        queryset = queryset.filter(is_active=True)

    if _model_has_field(TeacherOrganization, "status"):
        queryset = queryset.exclude(status="archived")

    if not _model_has_field(TeacherOrganization, "organization"):
        return

    organization_ids.update(
        organization_id
        for organization_id in queryset.values_list(
            "organization_id",
            flat=True,
        )
        if organization_id
    )


def _collect_learner_organizations(
    *,
    user: User,
    organization_ids: set[int],
) -> None:
    """
    Собирает организации обучающегося через академические зачисления.
    """

    LearnerGroupEnrollment = _get_model_or_none(
        "education",
        "LearnerGroupEnrollment",
    )

    if LearnerGroupEnrollment is None:
        return

    learner_field = _get_first_existing_field_name(
        LearnerGroupEnrollment,
        [
            "learner",
            "student",
            "user",
        ],
    )

    if learner_field is None:
        return

    organization_field_path = _get_group_organization_field_path(
        LearnerGroupEnrollment,
    )

    if organization_field_path is None:
        return

    queryset = LearnerGroupEnrollment.objects.filter(**{learner_field: user})

    if _model_has_field(LearnerGroupEnrollment, "status"):
        queryset = queryset.exclude(status="archived")

    organization_ids.update(
        organization_id
        for organization_id in queryset.values_list(
            organization_field_path,
            flat=True,
        )
        if organization_id
    )


def _collect_curator_organizations(
    *,
    user: User,
    organization_ids: set[int],
) -> None:
    """
    Собирает организации куратора.
    """

    GroupCurator = _get_model_or_none("organizations", "GroupCurator")

    if GroupCurator is None:
        return

    curator_field = _get_first_existing_field_name(
        GroupCurator,
        [
            "curator",
            "teacher",
            "user",
            "employee",
        ],
    )

    if curator_field is None:
        return

    organization_field_path = _get_group_organization_field_path(GroupCurator)

    if organization_field_path is None:
        return

    queryset = GroupCurator.objects.filter(**{curator_field: user})

    if _model_has_field(GroupCurator, "is_active"):
        queryset = queryset.filter(is_active=True)

    if _model_has_field(GroupCurator, "status"):
        queryset = queryset.exclude(status="archived")

    organization_ids.update(
        organization_id
        for organization_id in queryset.values_list(
            organization_field_path,
            flat=True,
        )
        if organization_id
    )


def _get_model_or_none(
    app_label: str,
    model_name: str,
):
    """
    Безопасно получает модель из app registry.
    """

    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        return None


def _model_has_field(
    model,
    field_name: str,
) -> bool:
    """
    Проверяет наличие поля в модели.
    """

    return any(field.name == field_name for field in model._meta.fields)


def _get_first_existing_field_name(
    model,
    field_names: list[str],
) -> str | None:
    """
    Возвращает первое существующее имя поля модели.
    """

    existing_field_names = {field.name for field in model._meta.fields}

    for field_name in field_names:
        if field_name in existing_field_names:
            return field_name

    return None


def _get_group_organization_field_path(model) -> str | None:
    """
    Возвращает путь до организации через поле group.
    """

    if not _model_has_field(model, "group"):
        return None

    group_field = model._meta.get_field("group")
    group_model = group_field.remote_field.model

    if _model_has_field(group_model, "organization"):
        return "group__organization_id"

    if not _model_has_field(group_model, "department"):
        return None

    department_field = group_model._meta.get_field("department")
    department_model = department_field.remote_field.model

    if _model_has_field(department_model, "organization"):
        return "group__department__organization_id"

    return None
