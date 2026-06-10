from __future__ import annotations

from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response


class EducationReadWriteViewSetMixin(viewsets.ModelViewSet):
    """
    Базовый ViewSet академического модуля.

    Разделяет сериализаторы чтения и записи:
    - create/update используют write serializer;
    - ответы возвращаются через read serializer.
    """

    filter_backends = (DjangoFilterBackend,)

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        """
        Возвращает сериализатор под действие.
        """

        if self.action in {
            "create",
            "update",
            "partial_update",
        }:
            return self.write_serializer_class

        return self.read_serializer_class

    def create(self, request, *args: Any, **kwargs: Any) -> Response:
        """
        Создаёт объект и возвращает read-представление.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        read_serializer = self.read_serializer_class(
            instance,
            context=self.get_serializer_context(),
        )

        return Response(
            read_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args: Any, **kwargs: Any) -> Response:
        """
        Обновляет объект и возвращает read-представление.
        """

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        read_serializer = self.read_serializer_class(
            instance,
            context=self.get_serializer_context(),
        )

        return Response(read_serializer.data)

    def build_read_response(
        self,
        instance,
        *,
        response_status: int = status.HTTP_200_OK,
    ) -> Response:
        """
        Возвращает объект через read serializer.
        """

        serializer = self.read_serializer_class(
            instance,
            context=self.get_serializer_context(),
        )

        return Response(
            serializer.data,
            status=response_status,
        )
