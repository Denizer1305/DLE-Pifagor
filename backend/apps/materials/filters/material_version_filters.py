from __future__ import annotations

import django_filters
from apps.materials.models import MaterialVersion
from django.db.models import Q


class MaterialVersionFilter(django_filters.FilterSet):
    """
    Фильтры версий учебных материалов.
    """

    search = django_filters.CharFilter(method="filter_search")

    material_id = django_filters.NumberFilter(
        field_name="material_id",
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=MaterialVersion.StatusChoices.choices,
    )
    created_by_id = django_filters.NumberFilter(
        field_name="created_by_id",
    )
    is_current = django_filters.BooleanFilter(
        field_name="is_current",
    )
    version_number = django_filters.NumberFilter(
        field_name="version_number",
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

    class Meta:
        model = MaterialVersion
        fields = (
            "search",
            "material_id",
            "status",
            "created_by_id",
            "is_current",
            "version_number",
            "created_after",
            "created_before",
            "updated_after",
            "updated_before",
        )

    def filter_search(
        self,
        queryset,
        name: str,
        value: str,
    ):
        """
        Ищет версию материала по материалу, файлу, ссылке и автору.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(material__title__icontains=value)
            | Q(material__slug__icontains=value)
            | Q(original_filename__icontains=value)
            | Q(mime_type__icontains=value)
            | Q(checksum__icontains=value)
            | Q(change_log__icontains=value)
            | Q(external_url__icontains=value)
            | Q(created_by__email__icontains=value)
            | Q(created_by__first_name__icontains=value)
            | Q(created_by__last_name__icontains=value)
        )
