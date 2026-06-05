from rest_framework import serializers


class UserSettingsPayloadSerializer(serializers.Serializer):
    appearance = serializers.DictField()
    notifications = serializers.DictField()
    privacy = serializers.DictField()
    security = serializers.DictField()
    roles = serializers.DictField()
