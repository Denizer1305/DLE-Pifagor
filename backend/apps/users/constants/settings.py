"""
Константы пользовательских настроек.

Файл содержит допустимые значения для персональных настроек пользователя:
внешний вид, уведомления, приватность, безопасность и ролевое поведение.
"""

from __future__ import annotations


class AppearanceTheme:
    """
    Доступные цветовые схемы интерфейса.
    """

    LIGHT = "light"
    BLUE = "blue"
    LIGHT_BLUE = "light-blue"
    GREEN = "green"
    ORANGE = "orange"
    PINKI = "pinki"
    VIOLET = "violet"
    RED = "red"
    YELLOW = "yellow"
    DARK = "dark"


class ColorMode:
    """
    Доступные режимы отображения интерфейса.
    """

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class InterfaceDensity:
    """
    Доступные режимы плотности интерфейса.
    """

    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    SPACIOUS = "spacious"


class InterfaceLanguage:
    """
    Доступные языки интерфейса.
    """

    RUSSIAN = "ru"
    ENGLISH = "en"
    GERMAN = "de"
    FRENCH = "fr"


class NotificationChannel:
    """
    Доступные каналы доставки уведомлений.
    """

    IN_APP = "in_app"
    EMAIL = "email"
    VK = "vk"
    MAX = "max"


class NotificationFrequency:
    """
    Доступные частоты получения уведомлений.
    """

    INSTANT = "instant"
    DAILY = "daily"
    WEEKLY = "weekly"
    DISABLED = "disabled"


class NotificationCategory:
    """
    Категории уведомлений платформы.
    """

    SECURITY = "security"
    EDUCATION = "education"
    ASSIGNMENTS = "assignments"
    SCHEDULE = "schedule"
    FEEDBACK = "feedback"
    SYSTEM = "system"
    DIGEST = "digest"
    MARKETING = "marketing"


class ProfileVisibility:
    """
    Уровни видимости профиля пользователя.
    """

    PUBLIC = "public"
    ORGANIZATION = "organization"
    ROLE_ONLY = "role_only"
    PRIVATE = "private"


class SessionLifetimeMode:
    """
    Режимы длительности пользовательских сессий.
    """

    STANDARD = "standard"
    EXTENDED = "extended"
    STRICT = "strict"


class SettingsRoleCode:
    """
    Роли, для которых можно настраивать поведение интерфейса.
    """

    TEACHER = "teacher"
    LEARNER = "learner"
    GUARDIAN = "guardian"
    ADMIN = "admin"
