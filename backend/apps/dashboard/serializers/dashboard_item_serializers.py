from __future__ import annotations

from apps.dashboard.models import DashboardItem
from rest_framework import serializers


class DashboardItemSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="item_date")
    event_type = serializers.CharField(source="event_theme")

    class Meta:
        model = DashboardItem
        fields = (
            "id",
            "kind",
            "title",
            "text",
            "date",
            "event_type",
            "notification_enabled",
            "created_at",
        )


class DashboardItemCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="item_date")
    event_type = serializers.ChoiceField(
        source="event_theme",
        choices=DashboardItem.ThemeChoices.choices,
        required=False,
        default=DashboardItem.ThemeChoices.NEUTRAL,
    )

    class Meta:
        model = DashboardItem
        fields = (
            "kind",
            "title",
            "text",
            "date",
            "event_type",
            "notification_enabled",
        )

    def validate_title(self, value: str) -> str:
        title = value.strip()

        if not title:
            raise serializers.ValidationError("Укажите название.")

        return title

    def validate_text(self, value: str) -> str:
        return value.strip()
