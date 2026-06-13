from __future__ import annotations


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
        """

        if hasattr(self, "action") and self.action in self.permission_action_classes:
            return [
                permission()
                for permission in self.permission_action_classes[self.action]
            ]

        return super().get_permissions()
