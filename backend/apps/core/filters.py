import django_filters


class CreatedAtRangeFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по диапазону даты создания.

    Добавляет фильтры:
        created_at_after:
            Объекты, созданные после указанной даты.
        created_at_before:
            Объекты, созданные до указанной даты.
    """

    created_at_after = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Создано после",
    )
    created_at_before = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Создано до",
    )


class UpdatedAtRangeFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по диапазону даты обновления.

    Добавляет фильтры:
        updated_at_after:
            Объекты, обновлённые после указанной даты.
        updated_at_before:
            Объекты, обновлённые до указанной даты.
    """

    updated_at_after = django_filters.IsoDateTimeFilter(
        field_name="updated_at",
        lookup_expr="gte",
        label="Обновлено после",
    )
    updated_at_before = django_filters.IsoDateTimeFilter(
        field_name="updated_at",
        lookup_expr="lte",
        label="Обновлено до",
    )


class StatusFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по полю status.

    Требует, чтобы у модели было поле `status`.
    """

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="exact",
        label="Статус",
    )


class IsArchivedFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по архивным объектам.

    Ожидает, что у модели есть поле `archived_at`.
    """

    is_archived = django_filters.BooleanFilter(
        method="filter_is_archived",
        label="В архиве",
    )

    def filter_is_archived(self, queryset, name, value):
        """
        Фильтрует объекты по признаку архивности.

        Args:
            queryset:
                Исходный QuerySet.
            name:
                Имя фильтра.
            value:
                True — только архивные, False — только неархивные.

        Returns:
            QuerySet: Отфильтрованный QuerySet.
        """

        if value is True:
            return queryset.filter(archived_at__isnull=False)

        if value is False:
            return queryset.filter(archived_at__isnull=True)

        return queryset


class IsDeletedFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по мягко удалённым объектам.

    Ожидает, что у модели есть поле `deleted_at`.
    """

    is_deleted = django_filters.BooleanFilter(
        method="filter_is_deleted",
        label="Удалён",
    )

    def filter_is_deleted(self, queryset, name, value):
        """
        Фильтрует объекты по признаку мягкого удаления.

        Args:
            queryset:
                Исходный QuerySet.
            name:
                Имя фильтра.
            value:
                True — только удалённые, False — только неудалённые.

        Returns:
            QuerySet: Отфильтрованный QuerySet.
        """

        if value is True:
            return queryset.filter(deleted_at__isnull=False)

        if value is False:
            return queryset.filter(deleted_at__isnull=True)

        return queryset
