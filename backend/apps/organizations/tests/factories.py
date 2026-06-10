from __future__ import annotations

from apps.organizations.constants import (
    StudyForm,
    StudyGroupStatus,
    TeacherEmploymentType,
)
from apps.organizations.models import (
    Department,
    GroupCurator,
    Organization,
    StudyGroup,
    Subject,
    TeacherOrganization,
    TeacherSubject,
)
from apps.users.constants.lifecycle import ProfileStatus, UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import Role, TeacherProfile, UserRole
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def create_test_user(
    *,
    email: str,
    phone: str,
    password: str = "StrongPassword123!",
    first_name: str = "Иван",
    last_name: str = "Иванов",
    middle_name: str = "",
    is_active: bool = True,
    is_staff: bool = False,
    is_superuser: bool = False,
):
    """
    Создаёт тестового пользователя.
    """

    return User.objects.create_user(
        email=email,
        phone=phone,
        password=password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        is_active=is_active,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )


def get_or_create_role(
    *,
    code: str,
    label: str | None = None,
) -> Role:
    """
    Возвращает роль или создаёт её.
    """

    role, _ = Role.objects.update_or_create(
        code=code,
        defaults={
            "label": label or code,
            "description": "",
            "is_system": True,
            "is_active": True,
            "sort_order": 100,
        },
    )

    return role


def assign_user_role(
    *,
    user,
    role_code: str,
    organization: Organization | None = None,
    department: Department | None = None,
    group: StudyGroup | None = None,
    assigned_by=None,
) -> UserRole:
    """
    Назначает пользователю активную роль.
    """

    role = get_or_create_role(
        code=role_code,
        label=role_code,
    )

    user_role, _ = UserRole.objects.update_or_create(
        user=user,
        role=role,
        organization=organization,
        department=department,
        group=group,
        defaults={
            "status": UserRoleStatus.ACTIVE,
            "assigned_by": assigned_by or user,
        },
    )

    return user_role


def create_superadmin(
    *,
    email: str = "superadmin@example.com",
    phone: str = "+79990000001",
):
    """
    Создаёт суперадминистратора.
    """

    user = create_test_user(
        email=email,
        phone=phone,
        first_name="Супер",
        last_name="Админ",
        is_staff=True,
        is_superuser=True,
    )

    assign_user_role(
        user=user,
        role_code=RoleCode.SUPERADMIN,
        assigned_by=user,
    )

    return user


def create_organization(
    *,
    name: str = "ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
    short_name: str = "ВлГК им. Советкина",
    code: str = "vlgk_sovetkina",
    slug: str = "vlgk-sovetkina",
    city: str = "Владимир",
    is_active: bool = True,
    is_public: bool = True,
    is_default_public: bool = False,
) -> Organization:
    """
    Создаёт образовательную организацию.
    """

    return Organization.objects.create(
        name=name,
        short_name=short_name,
        code=code,
        slug=slug,
        city=city,
        is_active=is_active,
        is_public=is_public,
        is_default_public=is_default_public,
    )


def create_department(
    *,
    organization: Organization,
    name: str = "Отделение информационных технологий",
    short_name: str = "ИТ-отделение",
    code: str = "it",
    is_active: bool = True,
) -> Department:
    """
    Создаёт отделение.
    """

    return Department.objects.create(
        organization=organization,
        name=name,
        short_name=short_name,
        code=code,
        is_active=is_active,
    )


def create_study_group(
    *,
    organization: Organization,
    department: Department | None = None,
    name: str = "ИС-21",
    code: str = "is_21",
    admission_year: int = 2023,
    graduation_year: int = 2027,
    course_number: int = 2,
    study_form: str = StudyForm.FULL_TIME,
    status: str = StudyGroupStatus.ACTIVE,
) -> StudyGroup:
    """
    Создаёт учебную группу.
    """

    return StudyGroup.objects.create(
        organization=organization,
        department=department,
        name=name,
        code=code,
        admission_year=admission_year,
        graduation_year=graduation_year,
        course_number=course_number,
        study_form=study_form,
        status=status,
    )


def create_subject(
    *,
    name: str = "Математика",
    short_name: str = "Математика",
    code: str = "math",
    is_active: bool = True,
) -> Subject:
    """
    Создаёт учебный предмет.
    """

    return Subject.objects.create(
        name=name,
        short_name=short_name,
        code=code,
        is_active=is_active,
    )


def create_teacher(
    *,
    organization: Organization,
    department: Department | None = None,
    email: str = "teacher@example.com",
    phone: str = "+79990000002",
    first_name: str = "Иван",
    last_name: str = "Иванов",
    middle_name: str = "Иванович",
    position: str = "Преподаватель",
    is_public: bool = True,
    show_on_teachers_page: bool = True,
    status: str = ProfileStatus.VERIFIED,
):
    """
    Создаёт пользователя-преподавателя с профилем и ролью.
    """

    user = create_test_user(
        email=email,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
    )

    assign_user_role(
        user=user,
        role_code=RoleCode.TEACHER,
        organization=organization,
    )

    TeacherProfile.objects.create(
        user=user,
        organization=organization,
        department=department,
        status=status,
        position=position,
        public_title=position,
        short_bio="Краткое описание преподавателя.",
        achievements="Достижение 1\nДостижение 2",
        experience_years=5,
        is_public=is_public,
        show_on_teachers_page=show_on_teachers_page,
    )

    return user


def create_teacher_subject(
    *,
    teacher,
    subject: Subject,
    is_primary: bool = True,
    is_active: bool = True,
) -> TeacherSubject:
    """
    Связывает преподавателя с предметом.
    """

    return TeacherSubject.objects.create(
        teacher=teacher,
        subject=subject,
        is_primary=is_primary,
        is_active=is_active,
    )


def create_teacher_organization(
    *,
    teacher,
    organization: Organization,
    position: str = "Преподаватель",
    employment_type: str = TeacherEmploymentType.FULL_TIME,
    is_primary: bool = True,
    is_active: bool = True,
) -> TeacherOrganization:
    """
    Создаёт связь преподавателя с организацией.
    """

    return TeacherOrganization.objects.create(
        teacher=teacher,
        organization=organization,
        position=position,
        employment_type=employment_type,
        is_primary=is_primary,
        is_active=is_active,
        starts_at=timezone.localdate(),
    )


def create_group_curator(
    *,
    group: StudyGroup,
    teacher,
    is_primary: bool = True,
    is_active: bool = True,
) -> GroupCurator:
    """
    Назначает куратора группе.
    """

    return GroupCurator.objects.create(
        group=group,
        teacher=teacher,
        is_primary=is_primary,
        is_active=is_active,
        starts_at=timezone.localdate(),
    )
