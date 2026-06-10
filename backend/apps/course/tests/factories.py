from __future__ import annotations

from datetime import date, timedelta
from uuid import uuid4

from apps.course.models import (
    Course,
    CourseAccessRule,
    CourseEnrollment,
    CourseGroupAccess,
    CourseLesson,
    CourseLessonBlock,
    CourseMaterialLink,
    CoursePlan,
    CoursePlanImport,
    CourseProgress,
    CourseSection,
    LessonProgress,
)
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Max
from django.utils import timezone

User = get_user_model()


def unique_code(prefix: str = "test") -> str:
    """
    Возвращает уникальный технический код.
    """

    return f"{prefix}_{uuid4().hex[:10]}"


def unique_slug(prefix: str = "test") -> str:
    """
    Возвращает уникальный slug.
    """

    return f"{prefix}-{uuid4().hex[:10]}"


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
    is_staff: bool = False,
    is_superuser: bool = False,
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
        "is_staff": is_staff,
        "is_superuser": is_superuser,
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


def create_superadmin(**overrides):
    """
    Создаёт суперпользователя.
    """

    return create_user(
        email=overrides.pop("email", "course-superadmin@example.com"),
        first_name=overrides.pop("first_name", "Супер"),
        last_name=overrides.pop("last_name", "Администратор"),
        is_staff=True,
        is_superuser=True,
        **overrides,
    )


def create_teacher(**overrides):
    """
    Создаёт пользователя с ролью преподавателя.
    """

    return create_user(
        email=overrides.pop("email", f"teacher_{uuid4().hex[:8]}@example.com"),
        role_code="teacher",
        first_name=overrides.pop("first_name", "Тестовый"),
        last_name=overrides.pop("last_name", "Преподаватель"),
        **overrides,
    )


def create_learner(**overrides):
    """
    Создаёт пользователя с ролью обучающегося.
    """

    return create_user(
        email=overrides.pop("email", f"learner_{uuid4().hex[:8]}@example.com"),
        role_code="learner",
        first_name=overrides.pop("first_name", "Тестовый"),
        last_name=overrides.pop("last_name", "Обучающийся"),
        **overrides,
    )


def create_organization(**overrides):
    """
    Создаёт тестовую организацию.
    """

    Organization = apps.get_model("organizations", "Organization")

    code = overrides.pop("code", unique_code("org"))
    name = overrides.pop("name", f"Тестовая организация {code}")

    data = _build_model_kwargs(
        Organization,
        name=name,
        short_name=overrides.pop("short_name", f"ТО {code[-4:]}"),
        code=code,
        slug=overrides.pop("slug", code.replace("_", "-")),
        city=overrides.pop("city", "Владимир"),
        address=overrides.pop("address", "ул. Тестовая, 1"),
        email=overrides.pop("email", f"{code}@example.com"),
        phone=overrides.pop("phone", "+7 900 000-00-00"),
        is_active=overrides.pop("is_active", True),
        is_public=overrides.pop("is_public", True),
        is_default_public=overrides.pop("is_default_public", False),
        **overrides,
    )

    return Organization.objects.create(**data)


def create_department(**overrides):
    """
    Создаёт тестовое отделение организации.
    """

    Department = _get_model_or_none("organizations", "Department")

    if Department is None:
        return None

    organization = overrides.pop("organization", None) or create_organization()
    code = overrides.pop("code", unique_code("dep"))

    data = _build_model_kwargs(
        Department,
        organization=organization,
        name=overrides.pop("name", f"Тестовое отделение {code}"),
        short_name=overrides.pop("short_name", f"ОТД {code[-4:]}"),
        code=code,
        slug=overrides.pop("slug", code.replace("_", "-")),
        description=overrides.pop("description", ""),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return Department.objects.create(**data)


def create_study_group(**overrides):
    """
    Создаёт тестовую учебную группу.
    """

    Group = _get_model_or_none("organizations", "StudyGroup")
    Group = Group or _get_model_or_none("organizations", "Group")

    if Group is None:
        raise LookupError(
            "Не найдена модель учебной группы: "
            "organizations.StudyGroup или organizations.Group."
        )

    organization = overrides.pop("organization", None) or create_organization()
    department = overrides.pop("department", None)

    if department is None and _model_has_field(Group, "department"):
        department = create_department(organization=organization)

    code = overrides.pop("code", unique_code("group"))

    data = _build_model_kwargs(
        Group,
        organization=organization,
        department=department,
        name=overrides.pop("name", f"ИС-{code[-4:]}"),
        title=overrides.pop("title", f"ИС-{code[-4:]}"),
        code=code,
        slug=overrides.pop("slug", code.replace("_", "-")),
        course_number=overrides.pop("course_number", 1),
        year_of_admission=overrides.pop("year_of_admission", 2026),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return Group.objects.create(**data)


def create_subject(**overrides):
    """
    Создаёт тестовый предмет.
    """

    Subject = apps.get_model("organizations", "Subject")

    code = overrides.pop("code", unique_code("subject"))

    data = _build_model_kwargs(
        Subject,
        name=overrides.pop("name", f"Предмет {code}"),
        short_name=overrides.pop("short_name", f"ПР {code[-4:]}"),
        code=code,
        description=overrides.pop("description", ""),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return Subject.objects.create(**data)


def create_academic_year(**overrides):
    """
    Создаёт учебный год.

    По умолчанию переиспользует один тестовый учебный год, чтобы не падать
    на уникальном ограничении is_current.
    """

    AcademicYear = apps.get_model("education", "AcademicYear")

    start_date = overrides.pop("start_date", date(2026, 9, 1))
    end_date = overrides.pop("end_date", date(2027, 6, 30))

    name = overrides.pop("name", f"{start_date.year}/{end_date.year}")
    code = overrides.pop("code", f"year_{start_date.year}_{end_date.year}")

    if not overrides:
        existing_year = AcademicYear.objects.filter(name=name).first()

        if existing_year is not None:
            return existing_year

    data = _build_model_kwargs(
        AcademicYear,
        name=name,
        code=code,
        start_date=start_date,
        end_date=end_date,
        is_active=overrides.pop("is_active", True),
        is_current=overrides.pop("is_current", True),
        **overrides,
    )

    return AcademicYear.objects.create(**data)


def create_education_period(
    *,
    academic_year=None,
    **overrides,
):
    """
    Создаёт учебный период.

    По умолчанию переиспользует период с sequence=1 внутри учебного года,
    чтобы не падать на уникальном ограничении:
    academic_year + sequence.
    """

    EducationPeriod = apps.get_model("education", "EducationPeriod")

    academic_year = academic_year or create_academic_year()

    start_date = overrides.pop("start_date", academic_year.start_date)
    end_date = overrides.pop(
        "end_date",
        date(academic_year.start_date.year, 12, 31),
    )

    sequence = overrides.pop(
        "sequence",
        overrides.pop("order", 1),
    )
    code = overrides.pop("code", f"period_{academic_year.id}_{sequence}")

    existing_period = EducationPeriod.objects.filter(
        academic_year=academic_year,
        sequence=sequence,
    ).first()

    if existing_period is not None:
        return existing_period

    data = _build_model_kwargs(
        EducationPeriod,
        academic_year=academic_year,
        name=overrides.pop("name", f"{sequence} семестр"),
        code=code,
        period_type=overrides.pop("period_type", "semester"),
        start_date=start_date,
        end_date=end_date,
        sequence=sequence,
        order=sequence,
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return EducationPeriod.objects.create(**data)


def create_group_subject(**overrides):
    """
    Создаёт связь группы с предметом.
    """

    GroupSubject = _get_model_or_none("education", "GroupSubject")

    if GroupSubject is None:
        return None

    group = overrides.pop("group", None) or create_study_group()
    subject = overrides.pop("subject", None) or create_subject()
    academic_year = overrides.pop("academic_year", None) or create_academic_year()

    data = _build_model_kwargs(
        GroupSubject,
        group=group,
        subject=subject,
        academic_year=academic_year,
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return GroupSubject.objects.create(**data)


def create_teacher_group_subject(**overrides):
    """
    Создаёт назначение преподавателя на предмет группы.
    """

    TeacherGroupSubject = _get_model_or_none(
        "education",
        "TeacherGroupSubject",
    )

    if TeacherGroupSubject is None:
        return None

    teacher = overrides.pop("teacher", None) or create_teacher()
    group_subject = overrides.pop("group_subject", None) or create_group_subject()

    group = overrides.pop("group", None)
    subject = overrides.pop("subject", None)

    if group_subject is not None:
        group = group or getattr(group_subject, "group", None)
        subject = subject or getattr(group_subject, "subject", None)

    data = _build_model_kwargs(
        TeacherGroupSubject,
        teacher=teacher,
        group_subject=group_subject,
        group=group,
        subject=subject,
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return TeacherGroupSubject.objects.create(**data)


def create_material(**overrides):
    """
    Создаёт учебный материал для связей курса.
    """

    Material = apps.get_model("materials", "Material")

    owner = overrides.pop("owner", None) or create_teacher()
    slug = overrides.pop("slug", unique_slug("material"))

    material_type = overrides.pop(
        "material_type",
        _choice_value(Material, "MaterialTypeChoices", "TEXT", "text"),
    )
    status = overrides.pop(
        "status",
        _choice_value(Material, "StatusChoices", "PUBLISHED", "published"),
    )
    visibility = overrides.pop(
        "visibility",
        _choice_value(Material, "VisibilityChoices", "PUBLIC", "public"),
    )
    source = overrides.pop(
        "source",
        _choice_value(Material, "SourceChoices", "MANUAL", "manual"),
    )

    data = _build_model_kwargs(
        Material,
        title=overrides.pop("title", "Тестовый материал"),
        slug=slug,
        short_description=overrides.pop("short_description", ""),
        description=overrides.pop("description", ""),
        material_type=material_type,
        status=status,
        visibility=visibility,
        source=source,
        organization=overrides.pop("organization", None),
        subject=overrides.pop("subject", None),
        category=overrides.pop("category", None),
        owner=owner,
        tags=overrides.pop("tags", []),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return Material.objects.create(**data)


def create_course(**overrides) -> Course:
    """
    Создаёт курс.
    """

    owner_teacher = overrides.pop("owner_teacher", None) or create_teacher()
    organization = overrides.pop("organization", None) or create_organization()
    subject = overrides.pop("subject", None) or create_subject()
    academic_year = overrides.pop("academic_year", None) or create_academic_year()
    period = overrides.pop(
        "period",
        None,
    ) or create_education_period(academic_year=academic_year)

    code = overrides.pop("code", unique_code("course"))
    slug = overrides.pop("slug", unique_slug("course"))

    data = _build_model_kwargs(
        Course,
        code=code,
        slug=slug,
        title=overrides.pop("title", f"Тестовый курс {code}"),
        subtitle=overrides.pop("subtitle", ""),
        description=overrides.pop("description", "Описание тестового курса."),
        course_type=overrides.pop(
            "course_type",
            _choice_value(Course, "CourseTypeChoices", "ACADEMIC", "academic"),
        ),
        origin=overrides.pop(
            "origin",
            _choice_value(Course, "OriginChoices", "MANUAL", "manual"),
        ),
        status=overrides.pop(
            "status",
            _choice_value(Course, "StatusChoices", "DRAFT", "draft"),
        ),
        visibility=overrides.pop(
            "visibility",
            _choice_value(Course, "VisibilityChoices", "PRIVATE", "private"),
        ),
        level=overrides.pop("level", "Базовый"),
        language=overrides.pop("language", "ru"),
        owner_teacher=owner_teacher,
        organization=organization,
        subject=subject,
        academic_year=academic_year,
        period=period,
        is_template=overrides.pop("is_template", False),
        is_active=overrides.pop("is_active", True),
        allow_self_enrollment=overrides.pop("allow_self_enrollment", False),
        enrollment_code=overrides.pop("enrollment_code", unique_code("enroll")),
        starts_at=overrides.pop("starts_at", timezone.now()),
        ends_at=overrides.pop("ends_at", timezone.now() + timedelta(days=90)),
        **overrides,
    )

    return Course.objects.create(**data)


def create_published_course(**overrides) -> Course:
    """
    Создаёт опубликованный курс.
    """

    return create_course(
        status=overrides.pop(
            "status",
            _choice_value(Course, "StatusChoices", "PUBLISHED", "published"),
        ),
        visibility=overrides.pop(
            "visibility",
            _choice_value(Course, "VisibilityChoices", "PUBLIC", "public"),
        ),
        is_active=overrides.pop("is_active", True),
        published_at=overrides.pop("published_at", timezone.now()),
        **overrides,
    )


def create_course_plan(
    *,
    course: Course | None = None,
    **overrides,
) -> CoursePlan:
    """
    Создаёт КТП курса.
    """

    course = course or create_course()

    data = _build_model_kwargs(
        CoursePlan,
        course=course,
        discipline_name=overrides.pop(
            "discipline_name",
            "Основы программирования",
        ),
        discipline_code=overrides.pop("discipline_code", "ОП.01"),
        specialty_code=overrides.pop("specialty_code", "09.02.07"),
        specialty_name=overrides.pop(
            "specialty_name",
            "Информационные системы и программирование",
        ),
        teacher_name_snapshot=overrides.pop(
            "teacher_name_snapshot",
            "Тестовый Преподаватель",
        ),
        organization_name_snapshot=overrides.pop(
            "organization_name_snapshot",
            "Тестовая организация",
        ),
        academic_year_label=overrides.pop("academic_year_label", "2026/2027"),
        semester_number=overrides.pop("semester_number", 1),
        total_hours=overrides.pop("total_hours", 72),
        semester_hours=overrides.pop("semester_hours", 72),
        theory_hours=overrides.pop("theory_hours", 30),
        practice_hours=overrides.pop("practice_hours", 30),
        lab_hours=overrides.pop("lab_hours", 12),
        self_study_hours=overrides.pop("self_study_hours", 0),
        consultation_hours=overrides.pop("consultation_hours", 0),
        commission_name=overrides.pop("commission_name", ""),
        protocol_number=overrides.pop("protocol_number", ""),
        protocol_date=overrides.pop("protocol_date", None),
        approved_order_number=overrides.pop("approved_order_number", ""),
        approved_order_date=overrides.pop("approved_order_date", None),
        status=overrides.pop(
            "status",
            _choice_value(CoursePlan, "StatusChoices", "DRAFT", "draft"),
        ),
        is_active=overrides.pop("is_active", True),
        notes=overrides.pop("notes", ""),
        **overrides,
    )

    return CoursePlan.objects.create(**data)


def create_course_plan_import(
    *,
    course_plan: CoursePlan | None = None,
    **overrides,
) -> CoursePlanImport:
    """
    Создаёт импорт КТП.
    """

    course_plan = course_plan or create_course_plan()

    source_file = overrides.pop(
        "source_file",
        SimpleUploadedFile(
            "ktp-test.pdf",
            b"%PDF-1.4\n% test ktp file content\n",
            content_type="application/pdf",
        ),
    )

    data = _build_model_kwargs(
        CoursePlanImport,
        course_plan=course_plan,
        source_file=source_file,
        original_filename=overrides.pop("original_filename", "ktp.pdf"),
        file_hash=overrides.pop("file_hash", uuid4().hex),
        status=overrides.pop(
            "status",
            _choice_value(
                CoursePlanImport,
                "StatusChoices",
                "UPLOADED",
                "uploaded",
            ),
        ),
        parser_version=overrides.pop("parser_version", "test-parser-1"),
        parsed_payload=overrides.pop("parsed_payload", {}),
        errors=overrides.pop("errors", []),
        imported_by=overrides.pop("imported_by", None) or create_teacher(),
        applied_at=overrides.pop("applied_at", None),
        **overrides,
    )

    return CoursePlanImport.objects.create(**data)


def create_course_section(
    *,
    course: Course | None = None,
    **overrides,
) -> CourseSection:
    """
    Создаёт раздел курса.
    """

    course = course or create_course()

    section_number = overrides.pop("section_number", None)

    if section_number is None:
        max_section_number = (
            CourseSection.objects.filter(course=course).aggregate(
                value=Max("section_number"),
            )["value"]
            or 0
        )
        section_number = max_section_number + 1

    data = _build_model_kwargs(
        CourseSection,
        course=course,
        title=overrides.pop("title", f"Раздел {section_number}"),
        description=overrides.pop("description", ""),
        section_number=section_number,
        order=overrides.pop("order", section_number),
        planned_hours=overrides.pop("planned_hours", 12),
        is_required=overrides.pop("is_required", True),
        is_published=overrides.pop("is_published", False),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return CourseSection.objects.create(**data)


def create_course_lesson(
    *,
    course: Course | None = None,
    section: CourseSection | None = None,
    **overrides,
) -> CourseLesson:
    """
    Создаёт урок курса.
    """

    course = course or create_course()

    if section is None:
        section = create_course_section(course=course)

    lesson_number = overrides.pop("lesson_number", None)

    if lesson_number is None:
        max_lesson_number = (
            CourseLesson.objects.filter(course=course).aggregate(
                value=Max("lesson_number"),
            )["value"]
            or 0
        )
        lesson_number = max_lesson_number + 1

    data = _build_model_kwargs(
        CourseLesson,
        course=course,
        section=section,
        lesson_number=lesson_number,
        lesson_type=overrides.pop(
            "lesson_type",
            _choice_value(
                CourseLesson,
                "LessonTypeChoices",
                "LECTURE",
                "lecture",
            ),
        ),
        title=overrides.pop("title", f"Урок {lesson_number}"),
        short_content=overrides.pop(
            "short_content",
            "Краткое содержание урока.",
        ),
        planned_hours=overrides.pop("planned_hours", 2),
        theory_hours=overrides.pop("theory_hours", 1),
        practice_hours=overrides.pop("practice_hours", 1),
        lab_hours=overrides.pop("lab_hours", 0),
        self_study_hours=overrides.pop("self_study_hours", 0),
        visual_aids=overrides.pop("visual_aids", ""),
        literature=overrides.pop("literature", ""),
        independent_work=overrides.pop("independent_work", ""),
        notes=overrides.pop("notes", ""),
        order=overrides.pop("order", lesson_number),
        available_from=overrides.pop("available_from", None),
        is_required=overrides.pop("is_required", True),
        is_preview=overrides.pop("is_preview", False),
        is_published=overrides.pop("is_published", True),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return CourseLesson.objects.create(**data)


def create_course_lesson_block(
    *,
    lesson: CourseLesson | None = None,
    **overrides,
) -> CourseLessonBlock:
    """
    Создаёт блок урока.
    """

    lesson = lesson or create_course_lesson()

    order = overrides.pop("order", None)

    if order is None:
        max_order = (
            CourseLessonBlock.objects.filter(lesson=lesson).aggregate(
                value=Max("order"),
            )["value"]
            or 0
        )
        order = max_order + 1

    block_type = overrides.pop(
        "block_type",
        _choice_value(
            CourseLessonBlock,
            "BlockTypeChoices",
            "TEXT",
            "text",
        ),
    )

    material = overrides.pop("material", None)

    if block_type == _choice_value(
        CourseLessonBlock,
        "BlockTypeChoices",
        "MATERIAL",
        "material",
    ):
        material = material or create_material()

    data = _build_model_kwargs(
        CourseLessonBlock,
        lesson=lesson,
        block_type=block_type,
        title=overrides.pop("title", f"Блок {order}"),
        content=overrides.pop("content", "Содержимое блока урока."),
        external_url=overrides.pop("external_url", ""),
        material=material,
        order=order,
        is_visible=overrides.pop("is_visible", True),
        **overrides,
    )

    return CourseLessonBlock.objects.create(**data)


def create_course_material_link(
    *,
    course: Course | None = None,
    section: CourseSection | None = None,
    lesson: CourseLesson | None = None,
    material=None,
    **overrides,
) -> CourseMaterialLink:
    """
    Создаёт связь курса с материалом.
    """

    course = course or create_course()

    if section is None:
        section = create_course_section(course=course)

    if lesson is None:
        lesson = create_course_lesson(course=course, section=section)

    material = material or create_material(
        organization=getattr(course, "organization", None),
        subject=getattr(course, "subject", None),
        owner=getattr(course, "owner_teacher", None),
    )

    data = _build_model_kwargs(
        CourseMaterialLink,
        course=course,
        section=section,
        lesson=lesson,
        material=material,
        placement=overrides.pop(
            "placement",
            _choice_value(CourseMaterialLink, "PlacementChoices", "LESSON", "lesson"),
        ),
        order=overrides.pop("order", 1),
        is_required=overrides.pop("is_required", False),
        is_visible=overrides.pop("is_visible", True),
        notes=overrides.pop("notes", ""),
        **overrides,
    )

    return CourseMaterialLink.objects.create(**data)


def create_course_group_access(
    *,
    course: Course | None = None,
    group=None,
    **overrides,
) -> CourseGroupAccess:
    """
    Создаёт групповой доступ к курсу.
    """

    course = course or create_course()
    group = group or create_study_group(
        organization=getattr(course, "organization", None),
    )

    data = _build_model_kwargs(
        CourseGroupAccess,
        course=course,
        group=group,
        group_subject=overrides.pop("group_subject", None),
        teacher_group_subject=overrides.pop("teacher_group_subject", None),
        visibility=overrides.pop(
            "visibility",
            _choice_value(CourseGroupAccess, "VisibilityChoices", "VISIBLE", "visible"),
        ),
        starts_at=overrides.pop("starts_at", None),
        ends_at=overrides.pop("ends_at", None),
        auto_enroll=overrides.pop("auto_enroll", True),
        is_active=overrides.pop("is_active", True),
        notes=overrides.pop("notes", ""),
        **overrides,
    )

    return CourseGroupAccess.objects.create(**data)


def create_course_access_rule(
    *,
    course: Course | None = None,
    learner=None,
    organization=None,
    **overrides,
) -> CourseAccessRule:
    """
    Создаёт правило доступа к курсу.
    """

    course = course or create_course()

    access_type = overrides.pop(
        "access_type",
        _choice_value(
            CourseAccessRule,
            "AccessTypeChoices",
            "LEARNER",
            "learner",
        ),
    )

    learner_access_type = _choice_value(
        CourseAccessRule,
        "AccessTypeChoices",
        "LEARNER",
        "learner",
    )
    organization_access_type = _choice_value(
        CourseAccessRule,
        "AccessTypeChoices",
        "ORGANIZATION",
        "organization",
    )

    if access_type == learner_access_type:
        learner = learner or create_learner()
        organization = None

    elif access_type == organization_access_type:
        learner = None
        organization = organization or getattr(course, "organization", None)

    else:
        learner = learner or None
        organization = organization or None

    data = _build_model_kwargs(
        CourseAccessRule,
        course=course,
        access_type=access_type,
        learner=learner,
        organization=organization,
        access_code=overrides.pop("access_code", unique_code("access")),
        starts_at=overrides.pop("starts_at", None),
        ends_at=overrides.pop("ends_at", None),
        auto_enroll=overrides.pop("auto_enroll", True),
        is_active=overrides.pop("is_active", True),
        notes=overrides.pop("notes", ""),
        **overrides,
    )

    return CourseAccessRule.objects.create(**data)


def create_course_enrollment(
    *,
    course: Course | None = None,
    learner=None,
    group_access: CourseGroupAccess | None = None,
    access_rule: CourseAccessRule | None = None,
    **overrides,
) -> CourseEnrollment:
    """
    Создаёт запись обучающегося на курс.
    """

    course = course or create_course()
    learner = learner or create_learner()

    initial_status = get_choice_value(
        CourseEnrollment,
        "StatusChoices",
        "NOT_STARTED",
        "ENROLLED",
        "ACTIVE",
        "IN_PROGRESS",
        default="active",
    )

    data = _build_model_kwargs(
        CourseEnrollment,
        course=course,
        learner=learner,
        group_access=group_access,
        access_rule=access_rule,
        status=overrides.pop("status", initial_status),
        enrolled_at=overrides.pop("enrolled_at", timezone.now()),
        started_at=overrides.pop("started_at", None),
        completed_at=overrides.pop("completed_at", None),
        last_activity_at=overrides.pop("last_activity_at", None),
        progress_percent=overrides.pop("progress_percent", 0),
        **overrides,
    )

    return CourseEnrollment.objects.create(**data)


def create_course_progress(
    *,
    enrollment: CourseEnrollment | None = None,
    **overrides,
) -> CourseProgress:
    """
    Создаёт общий прогресс курса.
    """

    enrollment = enrollment or create_course_enrollment()

    data = _build_model_kwargs(
        CourseProgress,
        enrollment=enrollment,
        progress_percent=overrides.pop("progress_percent", 0),
        total_lessons_count=overrides.pop("total_lessons_count", 0),
        completed_lessons_count=overrides.pop("completed_lessons_count", 0),
        last_lesson=overrides.pop("last_lesson", None),
        last_activity_at=overrides.pop("last_activity_at", None),
        **overrides,
    )

    progress, _ = CourseProgress.objects.get_or_create(
        enrollment=enrollment,
        defaults=data,
    )

    return progress


def create_lesson_progress(
    *,
    enrollment: CourseEnrollment | None = None,
    course_progress: CourseProgress | None = None,
    lesson: CourseLesson | None = None,
    **overrides,
) -> LessonProgress:
    """
    Создаёт прогресс урока.
    """

    enrollment = enrollment or create_course_enrollment()
    course_progress = course_progress or create_course_progress(
        enrollment=enrollment,
    )
    lesson = lesson or create_course_lesson(course=enrollment.course)

    data = _build_model_kwargs(
        LessonProgress,
        enrollment=enrollment,
        course_progress=course_progress,
        lesson=lesson,
        status=overrides.pop(
            "status",
            _choice_value(
                LessonProgress, "StatusChoices", "NOT_STARTED", "not_started"
            ),
        ),
        progress_percent=overrides.pop("progress_percent", 0),
        started_at=overrides.pop("started_at", None),
        completed_at=overrides.pop("completed_at", None),
        last_activity_at=overrides.pop("last_activity_at", None),
        **overrides,
    )

    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson,
        defaults=data,
    )

    return progress


def assign_role(
    *,
    user,
    role_code: str,
):
    """
    Назначает роль пользователю, если в users есть модели Role/UserRole.
    """

    Role = _get_model_or_none("users", "Role")
    UserRole = _get_model_or_none("users", "UserRole")

    if Role is None or UserRole is None:
        return None

    role_defaults = _build_model_kwargs(
        Role,
        name=role_code,
        description="",
        is_active=True,
    )
    role, _ = Role.objects.get_or_create(
        code=role_code,
        defaults=role_defaults,
    )

    user_role_defaults = _build_model_kwargs(
        UserRole,
        status="active",
        is_active=True,
    )

    lookup = _build_model_kwargs(
        UserRole,
        user=user,
        role=role,
    )

    if "user" not in lookup or "role" not in lookup:
        return None

    user_role, _ = UserRole.objects.get_or_create(
        **lookup,
        defaults=user_role_defaults,
    )

    return user_role


def get_choice_value(
    model,
    choices_name: str,
    *value_names: str,
    default: str = "",
) -> str:
    """
    Возвращает первое существующее значение enum.

    Нужен для тестов, чтобы не завязываться на конкретное имя статуса:
    NOT_STARTED / ACTIVE / ENROLLED и т.д.
    """

    choices_class = getattr(model, choices_name, None)

    if choices_class is None:
        return default

    for value_name in value_names:
        if hasattr(choices_class, value_name):
            return getattr(choices_class, value_name)

    choices = getattr(choices_class, "choices", ())

    if choices:
        return choices[0][0]

    return default


def _choice_value(
    model,
    choices_name: str,
    value_name: str,
    default: str,
) -> str:
    """
    Возвращает значение enum или fallback.
    """

    choices_class = getattr(model, choices_name, None)

    if choices_class is None:
        return default

    return getattr(choices_class, value_name, default)


def _build_model_kwargs(
    model,
    **kwargs,
) -> dict:
    """
    Оставляет только поля, которые реально принимает модель.

    Учитывает и field.name, и field.attname, поэтому допускает:
    - organization;
    - organization_id.
    """

    allowed_names = set()

    for field in model._meta.fields:
        allowed_names.add(field.name)
        allowed_names.add(field.attname)

    return {key: value for key, value in kwargs.items() if key in allowed_names}


def _model_has_field(
    model,
    field_name: str,
) -> bool:
    """
    Проверяет наличие поля в модели.
    """

    return any(field.name == field_name for field in model._meta.fields)


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
