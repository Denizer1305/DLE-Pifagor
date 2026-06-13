from __future__ import annotations


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

        Если для action указан метод в queryset_action_methods,
        вызывается он. Иначе используется стандартный get_queryset.
        """

        if hasattr(self, "action") and self.action in self.queryset_action_methods:
            method_name = self.queryset_action_methods[self.action]
            method = getattr(self, method_name)

            return method()

        return super().get_queryset()