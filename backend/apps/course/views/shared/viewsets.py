from __future__ import annotations

from typing import Any

from apps.course.models import Course
from apps.course.selectors import limit_courses_queryset_by_user
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response


class CourseReadWriteViewSetMixin(viewsets.ModelViewSet):
    """
    Базовый ViewSet модуля course.
    """

    filter_backends = (DjangoFilterBackend,)

    read_serializer_class = None
    write_serializer_class = None
    serializer_action_classes = {}

    def get_serializer_class(self):
        """
        Возвращает сериализатор под действие.
        """

        action_serializer = self.serializer_action_classes.get(self.action)

        if action_serializer is not None:
            return action_serializer

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

        return self.build_read_response(
            instance,
            response_status=status.HTTP_201_CREATED,
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

        return self.build_read_response(instance)

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


def filter_queryset_by_available_courses(
    *,
    queryset,
    user,
    course_field_path: str = "course",
):
    """
    Ограничивает queryset курсами, доступными пользователю.
    """

    available_courses = limit_courses_queryset_by_user(
        Course.objects.all(),
        user,
    )

    return queryset.filter(
        **{
            f"{course_field_path}__in": available_courses,
        }
    )
