from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class StudyGroupStatus(models.TextChoices):
    """
    Статусы учебной группы.

    ACTIVE:
        Группа действует и может принимать студентов.
    ARCHIVED:
        Группа скрыта из активной работы, но остаётся в истории.
    GRADUATED:
        Группа завершила обучение.
    CLOSED:
        Группа закрыта административно.
    """

    ACTIVE = "active", _("Активна")
    ARCHIVED = "archived", _("Архивирована")
    GRADUATED = "graduated", _("Выпущена")
    CLOSED = "closed", _("Закрыта")


class StudyForm(models.TextChoices):
    """
    Форма обучения учебной группы.
    """

    FULL_TIME = "full_time", _("Очная")
    PART_TIME = "part_time", _("Очно-заочная")
    EXTRAMURAL = "extramural", _("Заочная")
    DISTANCE = "distance", _("Дистанционная")
    OTHER = "other", _("Иная")


DEFAULT_GROUP_JOIN_CODE_TTL_DAYS = 30
"""
Срок действия кода вступления в группу в днях.
"""


MIN_GROUP_JOIN_CODE_LENGTH = 4
"""
Минимальная длина кода вступления в группу.
"""


MAX_GROUP_JOIN_CODE_LENGTH = 64
"""
Максимальная длина кода вступления в группу.
"""


GROUP_JOIN_CODE_PURPOSE = "group_join"
"""
Назначение кода вступления в группу.

Полезно для аудита, логов и будущих сервисов.
"""


MIN_COURSE_NUMBER = 1
"""
Минимальный номер курса.
"""


MAX_COURSE_NUMBER = 6
"""
Максимальный номер курса.

Для СПО обычно хватает 1-4, но оставляем запас под разные программы.
"""
