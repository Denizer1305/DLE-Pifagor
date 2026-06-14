from __future__ import annotations


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
        """

        if hasattr(self, "action") and self.action in self.serializer_action_classes:
            return self.serializer_action_classes[self.action]

        return super().get_serializer_class()
