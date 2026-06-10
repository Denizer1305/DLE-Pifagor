from __future__ import annotations

from datetime import date
from itertools import count
from typing import Any
from uuid import uuid4

from apps.education.models import (
    AcademicYear,
    Curriculum,
    CurriculumItem,
    EducationPeriod,
    GroupSubject,
    LearnerGroupEnrollment,
    TeacherGroupSubject,
)
from apps.organizations.models import Department, Organization, StudyGroup, Subject
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
ACADEMIC_YEAR_COUNTER = count(2030)


def _to_date(value) -> date:
    """
    Приводит строку ISO-формата или date к date.

    Нужен для factory, потому что в тестах удобно передавать
    как date(2026, 9, 1), так и строку "2026-09-01".
    """

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        return date.fromisoformat(value)

    return value


def unique_code(prefix: str) -> str:
    """
    Возвращает уникальный короткий код для тестовых данных.
    """

    return f"{prefix}_{uuid4().hex[:8]}"


def extract_results(payload):
    """
    Возвращает список объектов из paginated или обычного DRF-ответа.
    """

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in (
            "results",
            "items",
            "data",
            "objects",
            "content",
        ):
            value = payload.get(key)

            if isinstance(value, list):
                return value

        for value in payload.values():
            if isinstance(value, list):
                return value

    return []


def create_user(
    *,
    email: str | None = None,
    phone: str | None = None,
    role_code: str | None = None,
    first_name: str = "Тест",
    last_name: str = "Пользователь",
    password: str = "test-password",
    **extra_fields,
):
    """
    Создаёт пользователя и при необходимости назначает роль.
    """

    unique_suffix = uuid4().hex[:10]
    resolved_email = email or f"user_{unique_suffix}@example.com"

    numeric_suffix = uuid4().int % 10_000_000
    resolved_phone = phone or f"+7900{numeric_suffix:07d}"

    user_fields = {
        "email": resolved_email,
        "phone": resolved_phone,
        "first_name": first_name,
        "last_name": last_name,
        **extra_fields,
    }

    if _model_has_field(User, "username"):
        user_fields.setdefault("username", resolved_email)

    user_fields = _build_model_kwargs(
        User,
        **user_fields,
    )

    user = User.objects.create_user(
        password=password,
        **user_fields,
    )

    if role_code:
        assign_role(
            user=user,
            role_code=role_code,
        )

    return user


def assign_role(
    *,
    user,
    role_code: str,
):
    """
    Назначает роль пользователю устойчиво к текущей реализации users.
    """

    if role_code in {"superadmin", "platform_admin", "admin"}:
        if hasattr(user, "is_staff"):
            user.is_staff = True

        if hasattr(user, "is_superuser") and role_code == "superadmin":
            user.is_superuser = True

        user.save()

    Role = _get_model_or_none("users", "Role")
    UserRole = _get_model_or_none("users", "UserRole")

    role = None

    if Role is not None and _model_has_field(Role, "code"):
        role_defaults = _build_model_kwargs(
            Role,
            name=f"Роль {role_code}",
            title=f"Роль {role_code}",
            is_active=True,
        )

        role, _ = Role.objects.get_or_create(
            code=role_code,
            defaults=role_defaults,
        )

    if UserRole is not None and role is not None:
        user_role_kwargs = _build_model_kwargs(
            UserRole,
            user=user,
            role=role,
            status="active",
            is_active=True,
        )

        lookup = {
            "user": user,
            "role": role,
        }

        UserRole.objects.get_or_create(
            **lookup,
            defaults=user_role_kwargs,
        )

    user_roles = getattr(user, "roles", None)

    if user_roles is not None and role is not None:
        try:
            user_roles.add(role)
        except AttributeError:
            pass

    if _model_has_field(User, "role") and role is not None:
        user.role = role
        user.save(update_fields=["role"])


def create_organization(**overrides) -> Organization:
    """
    Создаёт тестовую организацию.
    """

    code = overrides.pop("code", unique_code("org"))
    name = overrides.pop("name", f"Тестовая организация {code}")
    short_name = overrides.pop("short_name", f"ТО {code[-4:]}")

    return _create_instance(
        Organization,
        name=name,
        short_name=short_name,
        code=code,
        slug=overrides.pop("slug", code),
        city=overrides.pop("city", "Владимир"),
        address=overrides.pop("address", "ул. Тестовая, 1"),
        email=overrides.pop("email", f"{code}@example.com"),
        phone=overrides.pop("phone", "+7 900 000-00-00"),
        is_active=overrides.pop("is_active", True),
        is_public=overrides.pop("is_public", True),
        is_default_public=overrides.pop("is_default_public", False),
        **overrides,
    )


def create_department(
    *,
    organization: Organization | None = None,
    **overrides,
) -> Department:
    """
    Создаёт тестовое отделение.
    """

    organization = organization or create_organization()
    code = overrides.pop("code", unique_code("dep"))

    return _create_instance(
        Department,
        organization=organization,
        name=overrides.pop("name", "Отделение тестирования"),
        short_name=overrides.pop("short_name", "ОТ"),
        code=code,
        description=overrides.pop("description", ""),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_study_group(
    *,
    organization: Organization | None = None,
    department: Department | None = None,
    **overrides,
) -> StudyGroup:
    """
    Создаёт тестовую учебную группу.
    """

    organization = organization or create_organization()
    department = department or create_department(organization=organization)
    code = overrides.pop("code", unique_code("group"))

    return _create_instance(
        StudyGroup,
        organization=organization,
        department=department,
        name=overrides.pop("name", "ИС-21"),
        code=code,
        admission_year=overrides.pop("admission_year", 2025),
        graduation_year=overrides.pop("graduation_year", 2029),
        course_number=overrides.pop("course_number", 1),
        study_form=overrides.pop("study_form", "full_time"),
        status=overrides.pop("status", "active"),
        is_active=overrides.pop("is_active", True),
        description=overrides.pop("description", ""),
        **overrides,
    )


def create_subject(**overrides) -> Subject:
    """
    Создаёт тестовый предмет.
    """

    code = overrides.pop("code", unique_code("subject"))
    name = overrides.pop("name", f"Предмет {code}")
    short_name = overrides.pop("short_name", f"ПР {code[-4:]}")

    return _create_instance(
        Subject,
        name=name,
        short_name=short_name,
        code=code,
        description=overrides.pop("description", ""),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_teacher_organization(
    *,
    teacher,
    organization: Organization,
):
    """
    Создаёт или возвращает связь преподавателя с организацией.
    """

    TeacherOrganization = _get_model_or_none(
        "organizations",
        "TeacherOrganization",
    )

    if TeacherOrganization is None:
        return None

    defaults = _build_model_kwargs(
        TeacherOrganization,
        position="Преподаватель",
        employment_type="full_time",
        is_primary=True,
        is_active=True,
        notes="",
    )

    return TeacherOrganization.objects.get_or_create(
        teacher=teacher,
        organization=organization,
        defaults=defaults,
    )[0]


def create_teacher_subject(
    *,
    teacher,
    subject: Subject,
):
    """
    Создаёт или возвращает связь преподавателя с предметом.
    """

    TeacherSubject = _get_model_or_none(
        "organizations",
        "TeacherSubject",
    )

    if TeacherSubject is None:
        return None

    defaults = _build_model_kwargs(
        TeacherSubject,
        is_primary=True,
        is_active=True,
        notes="",
    )

    return TeacherSubject.objects.get_or_create(
        teacher=teacher,
        subject=subject,
        defaults=defaults,
    )[0]


def create_academic_year(**overrides) -> AcademicYear:
    """
    Создаёт учебный год.
    """

    if "name" in overrides:
        name = overrides.pop("name")
        start_date = overrides.pop("start_date", date(int(name[:4]), 9, 1))
        end_date = overrides.pop("end_date", date(int(name[-4:]), 6, 30))
    else:
        start_year = next(ACADEMIC_YEAR_COUNTER)
        end_year = start_year + 1

        name = f"{start_year}/{end_year}"
        start_date = overrides.pop("start_date", date(start_year, 9, 1))
        end_date = overrides.pop("end_date", date(end_year, 6, 30))

    start_date = _to_date(start_date)
    end_date = _to_date(end_date)

    return AcademicYear.objects.create(
        name=name,
        start_date=start_date,
        end_date=end_date,
        description=overrides.pop("description", ""),
        is_current=overrides.pop("is_current", False),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_education_period(
    *,
    academic_year: AcademicYear | None = None,
    **overrides,
) -> EducationPeriod:
    """
    Создаёт учебный период.
    """

    academic_year = academic_year or create_academic_year()

    academic_year_start_date = _to_date(academic_year.start_date)
    academic_year_end_date = _to_date(academic_year.end_date)

    default_start_date = academic_year_start_date
    default_end_date = date(academic_year_start_date.year, 12, 31)

    if default_end_date <= default_start_date:
        default_end_date = academic_year_end_date

    start_date = _to_date(overrides.pop("start_date", default_start_date))
    end_date = _to_date(overrides.pop("end_date", default_end_date))

    return EducationPeriod.objects.create(
        academic_year=academic_year,
        name=overrides.pop("name", "1 семестр"),
        code=overrides.pop("code", unique_code("period")),
        period_type=overrides.pop(
            "period_type",
            EducationPeriod.PeriodTypeChoices.SEMESTER,
        ),
        sequence=overrides.pop("sequence", 1),
        start_date=start_date,
        end_date=end_date,
        description=overrides.pop("description", ""),
        is_current=overrides.pop("is_current", False),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_curriculum(
    *,
    organization: Organization | None = None,
    department: Department | None = None,
    academic_year: AcademicYear | None = None,
    **overrides,
) -> Curriculum:
    """
    Создаёт учебный план.
    """

    organization = organization or create_organization()
    department = department or create_department(organization=organization)
    academic_year = academic_year or create_academic_year()

    return Curriculum.objects.create(
        organization=organization,
        department=department,
        academic_year=academic_year,
        code=overrides.pop("code", unique_code("curriculum")),
        name=overrides.pop("name", "Учебный план ИС"),
        description=overrides.pop("description", ""),
        total_hours=overrides.pop("total_hours", 144),
        status=overrides.pop("status", Curriculum.StatusChoices.DRAFT),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_curriculum_item(
    *,
    curriculum: Curriculum | None = None,
    period: EducationPeriod | None = None,
    subject: Subject | None = None,
    **overrides,
) -> CurriculumItem:
    """
    Создаёт элемент учебного плана.
    """

    curriculum = curriculum or create_curriculum()
    period = period or create_education_period(
        academic_year=curriculum.academic_year,
    )
    subject = subject or create_subject()

    return CurriculumItem.objects.create(
        curriculum=curriculum,
        period=period,
        subject=subject,
        sequence=overrides.pop("sequence", 1),
        planned_hours=overrides.pop("planned_hours", 72),
        contact_hours=overrides.pop("contact_hours", 48),
        independent_hours=overrides.pop("independent_hours", 24),
        assessment_type=overrides.pop(
            "assessment_type",
            CurriculumItem.AssessmentTypeChoices.EXAM,
        ),
        is_required=overrides.pop("is_required", True),
        is_active=overrides.pop("is_active", True),
        notes=overrides.pop("notes", ""),
        **overrides,
    )


def create_group_subject(
    *,
    group: StudyGroup | None = None,
    subject: Subject | None = None,
    academic_year: AcademicYear | None = None,
    period: EducationPeriod | None = None,
    curriculum_item: CurriculumItem | None = None,
    **overrides,
) -> GroupSubject:
    """
    Создаёт предмет учебной группы.
    """

    group = group or create_study_group()

    if curriculum_item is not None:
        subject = subject or curriculum_item.subject
        academic_year = academic_year or curriculum_item.curriculum.academic_year
        period = period or curriculum_item.period

    subject = subject or create_subject()
    academic_year = academic_year or create_academic_year()
    period = period or create_education_period(academic_year=academic_year)

    return GroupSubject.objects.create(
        group=group,
        subject=subject,
        academic_year=academic_year,
        period=period,
        curriculum_item=curriculum_item,
        planned_hours=overrides.pop("planned_hours", 72),
        contact_hours=overrides.pop("contact_hours", 48),
        independent_hours=overrides.pop("independent_hours", 24),
        assessment_type=overrides.pop(
            "assessment_type",
            GroupSubject.AssessmentTypeChoices.EXAM,
        ),
        is_required=overrides.pop("is_required", True),
        is_active=overrides.pop("is_active", True),
        notes=overrides.pop("notes", ""),
        **overrides,
    )


def create_teacher_group_subject(
    *,
    teacher=None,
    group_subject: GroupSubject | None = None,
    **overrides,
) -> TeacherGroupSubject:
    """
    Создаёт назначение преподавателя на предмет группы.
    """

    group_subject = group_subject or create_group_subject()
    teacher = teacher or create_user(role_code="teacher")

    create_teacher_organization(
        teacher=teacher,
        organization=group_subject.group.organization,
    )
    create_teacher_subject(
        teacher=teacher,
        subject=group_subject.subject,
    )

    return TeacherGroupSubject.objects.create(
        teacher=teacher,
        group_subject=group_subject,
        role=overrides.pop(
            "role",
            TeacherGroupSubject.RoleChoices.PRIMARY,
        ),
        is_primary=overrides.pop("is_primary", True),
        is_active=overrides.pop("is_active", True),
        planned_hours=overrides.pop("planned_hours", 36),
        starts_at=overrides.pop("starts_at", group_subject.period.start_date),
        ends_at=overrides.pop("ends_at", group_subject.period.end_date),
        notes=overrides.pop("notes", ""),
        **overrides,
    )


def create_learner_group_enrollment(
    *,
    learner=None,
    group: StudyGroup | None = None,
    academic_year: AcademicYear | None = None,
    **overrides,
) -> LearnerGroupEnrollment:
    """
    Создаёт академическое зачисление обучающегося.
    """

    learner = learner or create_user(role_code="learner")
    group = group or create_study_group()
    academic_year = academic_year or create_academic_year()

    return LearnerGroupEnrollment.objects.create(
        learner=learner,
        group=group,
        academic_year=academic_year,
        enrollment_date=overrides.pop(
            "enrollment_date",
            academic_year.start_date,
        ),
        completion_date=overrides.pop("completion_date", None),
        status=overrides.pop(
            "status",
            LearnerGroupEnrollment.StatusChoices.ACTIVE,
        ),
        is_primary=overrides.pop("is_primary", True),
        journal_number=overrides.pop("journal_number", None),
        notes=overrides.pop("notes", ""),
        **overrides,
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


def _create_instance(
    model,
    **candidate_values,
):
    """
    Создаёт объект, передавая только существующие поля модели.
    """

    kwargs = _build_model_kwargs(model, **candidate_values)
    kwargs = _fill_required_defaults(model, kwargs)

    return model.objects.create(**kwargs)


def _build_model_kwargs(
    model,
    **candidate_values,
) -> dict[str, Any]:
    """
    Собирает kwargs только по существующим полям модели.
    """

    model_field_names = {field.name for field in model._meta.fields}

    return {
        field_name: value
        for field_name, value in candidate_values.items()
        if field_name in model_field_names
    }


def _fill_required_defaults(
    model,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    """
    Подставляет безопасные значения для обязательных простых полей.
    """

    resolved_kwargs = dict(kwargs)

    for field in model._meta.fields:
        if (
            field.primary_key
            or field.auto_created
            or field.name in resolved_kwargs
            or field.has_default()
            or field.null
            or field.blank
        ):
            continue

        if isinstance(field, models.ForeignKey):
            continue

        resolved_kwargs[field.name] = _default_value_for_field(field)

    return resolved_kwargs


def _default_value_for_field(field):
    """
    Возвращает тестовое значение для обязательного поля.
    """

    if field.choices:
        return field.choices[0][0]

    if isinstance(field, models.CharField):
        return unique_code(field.name)[: field.max_length]

    if isinstance(field, models.TextField):
        return ""

    if isinstance(field, models.BooleanField):
        return True

    if isinstance(field, models.PositiveIntegerField):
        return 1

    if isinstance(field, models.IntegerField):
        return 1

    if isinstance(field, models.DateField):
        return date(2025, 9, 1)

    return None
