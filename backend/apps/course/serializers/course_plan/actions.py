from __future__ import annotations

from rest_framework import serializers


class CoursePlanStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор изменения статуса КТП.

    Используется для действий:
    - review;
    - approve;
    - archive.
    """

    confirm = serializers.BooleanField(
        required=False,
        default=True,
    )
