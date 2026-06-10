from __future__ import annotations

from apps.materials.models import Material
from apps.materials.selectors.access_selectors import limit_materials_queryset_by_user
from django.db.models import Q, QuerySet


def material_base_queryset() -> QuerySet[Material]:
    """
    Возвращает базовый queryset материалов.
    """

    return Material.objects.select_related(
        "organization",
        "subject",
        "category",
        "owner",
        "current_version",
    )


def material_list_queryset(
    *,
    search: str | None = None,
    material_type: str | None = None,
    status: str | None = None,
    visibility: str | None = None,
    source: str | None = None,
    organization_id: int | None = None,
    subject_id: int | None = None,
    category_id: int | None = None,
    owner_id: int | None = None,
    is_active: bool | None = None,
) -> QuerySet[Material]:
    """
    Возвращает список учебных материалов.
    """

    queryset = material_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(slug__icontains=search)
            | Q(short_description__icontains=search)
            | Q(description__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(organization__short_name__icontains=search)
            | Q(subject__name__icontains=search)
            | Q(subject__short_name__icontains=search)
            | Q(subject__code__icontains=search)
            | Q(category__name__icontains=search)
            | Q(owner__email__icontains=search)
            | Q(owner__first_name__icontains=search)
            | Q(owner__last_name__icontains=search)
        )

    if material_type:
        queryset = queryset.filter(material_type=material_type)

    if status:
        queryset = queryset.filter(status=status)

    if visibility:
        queryset = queryset.filter(visibility=visibility)

    if source:
        queryset = queryset.filter(source=source)

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    if owner_id:
        queryset = queryset.filter(owner_id=owner_id)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "organization_id",
        "category_id",
        "-updated_at",
        "title",
    )


def material_detail_queryset() -> QuerySet[Material]:
    """
    Возвращает queryset материала с деталями.
    """

    return material_base_queryset().prefetch_related(
        "versions",
        "usage_logs",
    )


def get_material_by_id(
    material_id: int,
) -> Material:
    """
    Возвращает материал по идентификатору.
    """

    return material_detail_queryset().get(id=material_id)


def get_material_by_slug(
    slug: str,
) -> Material:
    """
    Возвращает материал по slug.
    """

    return material_detail_queryset().get(slug=slug)


def get_user_available_materials(
    *,
    user,
    search: str | None = None,
    material_type: str | None = None,
    status: str | None = None,
    visibility: str | None = None,
    source: str | None = None,
    organization_id: int | None = None,
    subject_id: int | None = None,
    category_id: int | None = None,
    is_active: bool | None = True,
) -> QuerySet[Material]:
    """
    Возвращает материалы, доступные пользователю.
    """

    queryset = material_list_queryset(
        search=search,
        material_type=material_type,
        status=status,
        visibility=visibility,
        source=source,
        organization_id=organization_id,
        subject_id=subject_id,
        category_id=category_id,
        is_active=is_active,
    )

    return limit_materials_queryset_by_user(queryset, user)


def get_owned_materials(
    *,
    owner_id: int,
    search: str | None = None,
    is_active: bool | None = None,
) -> QuerySet[Material]:
    """
    Возвращает материалы владельца.
    """

    return material_list_queryset(
        search=search,
        owner_id=owner_id,
        is_active=is_active,
    )


def get_published_public_materials(
    *,
    search: str | None = None,
    material_type: str | None = None,
) -> QuerySet[Material]:
    """
    Возвращает публичные опубликованные материалы.
    """

    from apps.materials.models import Material

    return material_list_queryset(
        search=search,
        material_type=material_type,
        status=Material.StatusChoices.PUBLISHED,
        visibility=Material.VisibilityChoices.PUBLIC,
        is_active=True,
    )
