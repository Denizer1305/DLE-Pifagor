from __future__ import annotations

import django_filters
from apps.materials.models import MaterialUsageLog
from django.db.models import Q


class MaterialUsageLogFilter(django_filters.FilterSet):
    """
    Фильтры журнала использования материалов.
    """

    search = django_filters.CharFilter(method="filter_search")

    material_id = django_filters.NumberFilter(
        field_name="material_id",
    )
    user_id = django_filters.NumberFilter(
        field_name="user_id",
    )
    action = django_filters.ChoiceFilter(
        field_name="action",
        choices=MaterialUsageLog.ActionChoices.choices,
    )
    context = django_filters.ChoiceFilter(
        field_name="context",
        choices=MaterialUsageLog.ContextChoices.choices,
    )
    context_object_id = django_filters.NumberFilter(
        field_name="context_object_id",
    )

    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    class Meta:
        model = MaterialUsageLog
        fields = (
            "search",
            "material_id",
            "user_id",
            "action",
            "context",
            "context_object_id",
            "created_after",
            "created_before",
        )

    def filter_search(
        self,
        queryset,
        name: str,
        value: str,
    ):
        """
        Ищет событие журнала по материалу, пользователю и техническим данным.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(material__title__icontains=value)
            | Q(material__slug__icontains=value)
            | Q(user__email__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(ip_address__icontains=value)
            | Q(user_agent__icontains=value)
        )
