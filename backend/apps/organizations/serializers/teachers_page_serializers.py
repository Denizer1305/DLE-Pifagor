from __future__ import annotations

from rest_framework import serializers


class PublicTeachersPageSerializer(serializers.Serializer):
    """
    Ответ для публичной страницы преподавателей.
    """

    organization = serializers.DictField()
    subjects = serializers.ListField()
    teachers = serializers.ListField()
    meta = serializers.DictField()
