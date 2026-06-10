from __future__ import annotations

from rest_framework import serializers


class CourseStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор изменения статуса курса.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )


class CourseDuplicateActionSerializer(serializers.Serializer):
    """
    Action-сериализатор копирования курса.
    """

    title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )
    code = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=64,
    )
    slug = serializers.SlugField(
        required=False,
        allow_blank=True,
        max_length=120,
    )
    copy_material_links = serializers.BooleanField(
        required=False,
        default=True,
    )


class CourseCreateWithPlanSerializer(serializers.Serializer):
    """
    Action-сериализатор создания курса вместе с КТП.
    """

    course = serializers.DictField()
    plan = serializers.DictField()
