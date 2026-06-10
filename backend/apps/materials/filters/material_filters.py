from __future__ import annotations

import django_filters
from apps.materials.models import Material
from django.db.models import Q


class MaterialFilter(django_filters.FilterSet):
    """
    Фильтры учебных материалов.
    """

    search = django_filters.CharFilter(method="filter_search")

    material_type = django_filters.ChoiceFilter(
        field_name="material_type",
        choices=Material.MaterialTypeChoices.choices,
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Material.StatusChoices.choices,
    )
    visibility = django_filters.ChoiceFilter(
        field_name="visibility",
        choices=Material.VisibilityChoices.choices,
    )
    source = django_filters.ChoiceFilter(
        field_name="source",
        choices=Material.SourceChoices.choices,
    )

    organization_id = django_filters.NumberFilter(
        field_name="organization_id",
    )
    subject_id = django_filters.NumberFilter(
        field_name="subject_id",
    )
    category_id = django_filters.NumberFilter(
        field_name="category_id",
    )
    owner_id = django_filters.NumberFilter(
        field_name="owner_id",
    )

    is_active = django_filters.BooleanFilter(
        field_name="is_active",
    )
    has_current_version = django_filters.BooleanFilter(
        method="filter_has_current_version",
    )
    global_only = django_filters.BooleanFilter(
        method="filter_global_only",
    )

    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )
    updated_after = django_filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="gte",
    )
    updated_before = django_filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="lte",
    )
    published_after = django_filters.DateTimeFilter(
        field_name="published_at",
        lookup_expr="gte",
    )
    published_before = django_filters.DateTimeFilter(
        field_name="published_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Material
        fields = (
            "search",
            "material_type",
            "status",
            "visibility",
            "source",
            "organization_id",
            "subject_id",
            "category_id",
            "owner_id",
            "is_active",
            "has_current_version",
            "global_only",
            "created_after",
            "created_before",
            "updated_after",
            "updated_before",
            "published_after",
            "published_before",
        )

    def filter_search(
        self,
        queryset,
        name: str,
        value: str,
    ):
        """
        Ищет материал по основным текстовым полям и связанным сущностям.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(slug__icontains=value)
            | Q(short_description__icontains=value)
            | Q(description__icontains=value)
            | Q(organization__name__icontains=value)
            | Q(organization__short_name__icontains=value)
            | Q(organization__code__icontains=value)
            | Q(subject__name__icontains=value)
            | Q(subject__short_name__icontains=value)
            | Q(subject__code__icontains=value)
            | Q(category__name__icontains=value)
            | Q(category__slug__icontains=value)
            | Q(owner__email__icontains=value)
            | Q(owner__first_name__icontains=value)
            | Q(owner__last_name__icontains=value)
        )

    def filter_has_current_version(
        self,
        queryset,
        name: str,
        value: bool,
    ):
        """
        Фильтрует материалы по наличию текущей версии.
        """

        if value:
            return queryset.filter(current_version__isnull=False)

        return queryset.filter(current_version__isnull=True)

    def filter_global_only(
        self,
        queryset,
        name: str,
        value: bool,
    ):
        """
        Оставляет только материалы без организации.
        """

        if value:
            return queryset.filter(organization__isnull=True)

        return queryset
