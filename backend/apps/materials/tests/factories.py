from __future__ import annotations

from uuid import uuid4

from apps.materials.models import (
    Material,
    MaterialCategory,
    MaterialUsageLog,
    MaterialVersion,
)
from django.apps import apps
from django.contrib.auth import get_user_model

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
    Создаёт суперпользователя для API-тестов.
    """

    return create_user(
        email=overrides.pop("email", "superadmin@example.com"),
        first_name=overrides.pop("first_name", "Супер"),
        last_name=overrides.pop("last_name", "Администратор"),
        is_staff=True,
        is_superuser=True,
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


def create_subject(**overrides):
    """
    Создаёт тестовый предмет.
    """

    Subject = apps.get_model("organizations", "Subject")

    code = overrides.pop("code", unique_code("subject"))
    name = overrides.pop("name", f"Предмет {code}")

    data = _build_model_kwargs(
        Subject,
        name=name,
        short_name=overrides.pop("short_name", f"ПР {code[-4:]}"),
        code=code,
        description=overrides.pop("description", ""),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )

    return Subject.objects.create(**data)


def create_material_category(**overrides) -> MaterialCategory:
    """
    Создаёт категорию материалов.
    """

    name = overrides.pop("name", "Тестовая категория")
    slug = overrides.pop("slug", unique_slug("category"))

    return MaterialCategory.objects.create(
        organization=overrides.pop("organization", None),
        parent=overrides.pop("parent", None),
        name=name,
        slug=slug,
        description=overrides.pop("description", ""),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_material(**overrides) -> Material:
    """
    Создаёт учебный материал.
    """

    title = overrides.pop("title", "Тестовый материал")
    slug = overrides.pop("slug", unique_slug("material"))

    return Material.objects.create(
        title=title,
        slug=slug,
        short_description=overrides.pop("short_description", ""),
        description=overrides.pop("description", ""),
        material_type=overrides.pop(
            "material_type",
            Material.MaterialTypeChoices.TEXT,
        ),
        status=overrides.pop("status", Material.StatusChoices.DRAFT),
        visibility=overrides.pop(
            "visibility",
            Material.VisibilityChoices.PRIVATE,
        ),
        source=overrides.pop("source", Material.SourceChoices.MANUAL),
        organization=overrides.pop("organization", None),
        subject=overrides.pop("subject", None),
        category=overrides.pop("category", None),
        owner=overrides.pop("owner", None),
        tags=overrides.pop("tags", []),
        is_active=overrides.pop("is_active", True),
        **overrides,
    )


def create_material_version(**overrides) -> MaterialVersion:
    """
    Создаёт версию учебного материала.
    """

    material = overrides.pop("material", None) or create_material()

    return MaterialVersion.objects.create(
        material=material,
        version_number=overrides.pop("version_number", 1),
        status=overrides.pop("status", MaterialVersion.StatusChoices.DRAFT),
        file=overrides.pop("file", None),
        external_url=overrides.pop("external_url", ""),
        content=overrides.pop("content", "Тестовое содержимое материала."),
        original_filename=overrides.pop("original_filename", ""),
        mime_type=overrides.pop("mime_type", "text/plain"),
        file_size_bytes=overrides.pop("file_size_bytes", None),
        checksum=overrides.pop("checksum", ""),
        created_by=overrides.pop("created_by", None),
        change_log=overrides.pop("change_log", ""),
        is_current=overrides.pop("is_current", False),
        **overrides,
    )


def create_material_usage_log(**overrides) -> MaterialUsageLog:
    """
    Создаёт событие журнала использования материала.
    """

    material = overrides.pop("material", None) or create_material()

    return MaterialUsageLog.objects.create(
        material=material,
        user=overrides.pop("user", None),
        action=overrides.pop("action", MaterialUsageLog.ActionChoices.VIEW),
        context=overrides.pop("context", MaterialUsageLog.ContextChoices.LIBRARY),
        context_object_id=overrides.pop("context_object_id", None),
        ip_address=overrides.pop("ip_address", ""),
        user_agent=overrides.pop("user_agent", ""),
        metadata=overrides.pop("metadata", {}),
        **overrides,
    )


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


def _build_model_kwargs(
    model,
    **kwargs,
) -> dict:
    """
    Оставляет только поля, которые реально есть в модели.
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
