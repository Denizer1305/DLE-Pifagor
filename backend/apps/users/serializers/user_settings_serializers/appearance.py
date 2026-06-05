from __future__ import annotations

from apps.users.constants.settings import (
    AppearanceTheme,
    ColorMode,
    InterfaceDensity,
    InterfaceLanguage,
)
from rest_framework import serializers

APPEARANCE_THEMES = {
    AppearanceTheme.LIGHT,
    AppearanceTheme.BLUE,
    AppearanceTheme.LIGHT_BLUE,
    AppearanceTheme.GREEN,
    AppearanceTheme.ORANGE,
    AppearanceTheme.PINKI,
    AppearanceTheme.VIOLET,
    AppearanceTheme.RED,
    AppearanceTheme.YELLOW,
    AppearanceTheme.DARK,
}

COLOR_MODES = {
    ColorMode.LIGHT,
    ColorMode.DARK,
    ColorMode.SYSTEM,
}

INTERFACE_DENSITIES = {
    InterfaceDensity.COMPACT,
    InterfaceDensity.COMFORTABLE,
    InterfaceDensity.SPACIOUS,
}

INTERFACE_LANGUAGES = {
    InterfaceLanguage.RUSSIAN,
    InterfaceLanguage.ENGLISH,
    InterfaceLanguage.GERMAN,
    InterfaceLanguage.FRENCH,
}


class AppearanceSettingsUpdateSerializer(serializers.Serializer):
    theme = serializers.CharField(required=False)
    color_mode = serializers.CharField(required=False)
    density = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    animations_enabled = serializers.BooleanField(required=False)
    glass_panels_enabled = serializers.BooleanField(required=False)
    rounded_cards_enabled = serializers.BooleanField(required=False)
    sticky_sidebar_enabled = serializers.BooleanField(required=False)
    large_cards_enabled = serializers.BooleanField(required=False)

    def validate_theme(self, value: str) -> str:
        if value not in APPEARANCE_THEMES:
            raise serializers.ValidationError("Недопустимая цветовая схема.")

        return value

    def validate_color_mode(self, value: str) -> str:
        if value not in COLOR_MODES:
            raise serializers.ValidationError("Недопустимый режим отображения.")

        return value

    def validate_density(self, value: str) -> str:
        if value not in INTERFACE_DENSITIES:
            raise serializers.ValidationError("Недопустимая плотность интерфейса.")

        return value

    def validate_language(self, value: str) -> str:
        if value not in INTERFACE_LANGUAGES:
            raise serializers.ValidationError("Недопустимый язык интерфейса.")

        return value
