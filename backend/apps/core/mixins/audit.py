from __future__ import annotations


class CreatedUpdatedBySerializerMixin:
    """
    Mixin для автоматической передачи created_by/updated_by в serializer.save().

    Используется во views, где нужно сохранять автора создания и обновления.
    """

    def perform_create(self, serializer):
        """
        Сохраняет объект с указанием пользователя, создавшего объект.
        """

        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """
        Сохраняет объект с указанием пользователя, изменившего объект.
        """

        serializer.save(updated_by=self.request.user)
