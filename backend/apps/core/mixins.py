class SerializerByActionMixin:
    """
    Mixin для выбора serializer_class по action.

    Используется во ViewSet, где для разных действий нужны разные serializers.

    Example:
        serializer_action_classes = {
            "list": UserListSerializer,
            "retrieve": UserDetailSerializer,
            "create": UserCreateSerializer,
        }
    """

    serializer_action_classes = {}

    def get_serializer_class(self):
        """
        Возвращает serializer_class для текущего action.

        Если для action serializer не найден, возвращается стандартный
        serializer_class родительского класса.

        Returns:
            type: Класс serializer.
        """

        if hasattr(self, "action") and self.action in self.serializer_action_classes:
            return self.serializer_action_classes[self.action]

        return super().get_serializer_class()


class PermissionByActionMixin:
    """
    Mixin для выбора permission_classes по action.

    Используется во ViewSet, где для разных действий нужны разные права.

    Example:
        permission_action_classes = {
            "list": [IsAdminUser],
            "retrieve": [IsAuthenticated],
        }
    """

    permission_action_classes = {}

    def get_permissions(self):
        """
        Возвращает список permission instances для текущего action.

        Если для action permissions не найдены, используется стандартное
        поведение родительского класса.

        Returns:
            list: Список объектов permissions.
        """

        if hasattr(self, "action") and self.action in self.permission_action_classes:
            return [
                permission()
                for permission in self.permission_action_classes[self.action]
            ]

        return super().get_permissions()


class QuerysetByActionMixin:
    """
    Mixin для выбора queryset по action.

    Подходит для ViewSet, где list/retrieve/custom actions должны
    использовать разные selectors или querysets.
    """

    queryset_action_methods = {}

    def get_queryset(self):
        """
        Возвращает queryset для текущего action.

        Если для action указан метод в `queryset_action_methods`,
        вызывается он. Иначе используется стандартный get_queryset.

        Returns:
            QuerySet: QuerySet для текущего действия.
        """

        if hasattr(self, "action") and self.action in self.queryset_action_methods:
            method_name = self.queryset_action_methods[self.action]
            method = getattr(self, method_name)
            return method()

        return super().get_queryset()


class CreatedUpdatedBySerializerMixin:
    """
    Mixin для автоматической передачи created_by/updated_by в serializer.save().

    Используется во views, где нужно сохранять автора создания и обновления.
    """

    def perform_create(self, serializer):
        """
        Сохраняет объект с указанием пользователя, создавшего объект.

        Args:
            serializer:
                DRF serializer.
        """

        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """
        Сохраняет объект с указанием пользователя, изменившего объект.

        Args:
            serializer:
                DRF serializer.
        """

        serializer.save(updated_by=self.request.user)
