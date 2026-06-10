from __future__ import annotations

from django.db import models


class MaterialUsageLogQuerySet(models.QuerySet):
    """
    QuerySet журнала использования материалов.
    """

    def for_material(self, material_id: int):
        """
        Фильтрует события по материалу.
        """

        return self.filter(material_id=material_id)

    def by_user(self, user_id: int):
        """
        Фильтрует события по пользователю.
        """

        return self.filter(user_id=user_id)

    def by_action(self, action: str):
        """
        Фильтрует события по действию.
        """

        return self.filter(action=action)

    def by_context(self, context: str):
        """
        Фильтрует события по контексту.
        """

        return self.filter(context=context)

    def ordered_recent(self):
        """
        Возвращает события от новых к старым.
        """

        return self.order_by("-created_at", "-id")


class MaterialUsageLogManager(models.Manager.from_queryset(MaterialUsageLogQuerySet)):
    """
    Менеджер журнала использования материалов.
    """

    use_in_migrations = False
