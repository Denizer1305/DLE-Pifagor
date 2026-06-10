from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class TeacherEmploymentType(models.TextChoices):
    """
    Тип занятости преподавателя в образовательной организации.
    """

    FULL_TIME = "full_time", _("Основное место работы")
    PART_TIME = "part_time", _("Совместительство")
    CONTRACT = "contract", _("Договор")
    OTHER = "other", _("Иное")
