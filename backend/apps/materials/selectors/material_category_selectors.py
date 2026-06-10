from __future__ import annotations

from apps.materials.models import MaterialCategory
from apps.materials.selectors.access_selectors import (
    limit_queryset_by_user_organizations,
)
from django.db.models import Q, QuerySet


def material_category_base_queryset() -> QuerySet[MaterialCategory]:
    """
    Возвращает базовый queryset категорий материалов.
    """

    return MaterialCategory.objects.select_related(
        "organization",
        "parent",
    )


def material_category_list_queryset(
    *,
    search: str | None = None,
    organization_id: int | None = None,
    parent_id: int | None = None,
    is_active: bool | None = None,
    include_global: bool = True,
) -> QuerySet[MaterialCategory]:
    """
    Возвращает список категорий материалов.
    """

    queryset = material_category_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(slug__icontains=search)
            | Q(description__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(organization__short_name__icontains=search)
        )

    if organization_id:
        query = Q(organization_id=organization_id)

        if include_global:
            query |= Q(organization__isnull=True)

        queryset = queryset.filter(query)

    if parent_id is not None:
        queryset = queryset.filter(parent_id=parent_id)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "organization_id",
        "parent_id",
        "name",
    )


def material_category_detail_queryset() -> QuerySet[MaterialCategory]:
    """
    Возвращает queryset категории с деталями.
    """

    return material_category_base_queryset().prefetch_related(
        "children",
        "materials",
    )


def get_material_category_by_id(
    category_id: int,
) -> MaterialCategory:
    """
    Возвращает категорию материала по идентификатору.
    """

    return material_category_detail_queryset().get(id=category_id)


def get_material_category_by_slug(
    slug: str,
    *,
    organization_id: int | None = None,
) -> MaterialCategory:
    """
    Возвращает категорию материала по slug.
    """

    queryset = material_category_detail_queryset().filter(slug=slug)

    if organization_id:
        queryset = queryset.filter(
            Q(organization_id=organization_id) | Q(organization__isnull=True)
        )
    else:
        queryset = queryset.filter(organization__isnull=True)

    return queryset.get()


def get_available_material_categories_for_user(
    *,
    user,
    search: str | None = None,
    organization_id: int | None = None,
    is_active: bool | None = True,
) -> QuerySet[MaterialCategory]:
    """
    Возвращает категории материалов, доступные пользователю.
    """

    queryset = material_category_list_queryset(
        search=search,
        organization_id=organization_id,
        is_active=is_active,
    )

    return limit_queryset_by_user_organizations(
        queryset,
        user,
        organization_field="organization_id",
        include_global=True,
    )
