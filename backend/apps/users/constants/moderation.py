from django.db import models


class ModerationStatus(models.TextChoices):
    """
    Статусы модерации пользовательских данных.

    Используется для:
        - аватара;
        - описания профиля;
        - публичной карточки преподавателя;
        - других данных, которые могут быть показаны другим пользователям.
    """

    NOT_SUBMITTED = "not_submitted", "Не отправлено"
    PENDING = "pending", "Ожидает модерации"
    APPROVED = "approved", "Одобрено"
    REJECTED = "rejected", "Отклонено"


class ModerationTarget(models.TextChoices):
    """
    Типы объектов модерации.
    """

    AVATAR = "avatar", "Аватар"
    PROFILE = "profile", "Профиль"
    TEACHER_PUBLIC_PROFILE = "teacher_public_profile", "Публичный профиль преподавателя"


class ModerationDecision(models.TextChoices):
    """
    Решения модератора.
    """

    APPROVE = "approve", "Одобрить"
    REJECT = "reject", "Отклонить"
    RETURN_FOR_EDIT = "return_for_edit", "Вернуть на доработку"


PENDING_MODERATION_STATUSES = {
    ModerationStatus.PENDING,
}
"""Статусы, которые ожидают модерации."""


APPROVED_MODERATION_STATUSES = {
    ModerationStatus.APPROVED,
}
"""Статусы, которые считаются успешно прошедшими модерацию."""


REJECTED_MODERATION_STATUSES = {
    ModerationStatus.REJECTED,
}
"""Статусы, которые считаются отклонёнными модерацией."""
