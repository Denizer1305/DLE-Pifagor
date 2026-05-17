from django.db import models


class UserStatus(models.TextChoices):
    """
    Статусы жизненного цикла пользователя.

    Эти статусы описывают состояние аккаунта пользователя
    от регистрации до возможной анонимизации.
    """

    PENDING_EMAIL = "pending_email", "Ожидает подтверждения email"
    PENDING_REVIEW = "pending_review", "Ожидает проверки"
    ACTIVE = "active", "Активен"
    REJECTED = "rejected", "Отклонён"
    BLOCKED = "blocked", "Заблокирован"
    ARCHIVED = "archived", "В архиве"
    SCHEDULED_FOR_DELETION = "scheduled_for_deletion", "Запланирован к удалению"
    ANONYMIZED = "anonymized", "Анонимизирован"


class UserRoleStatus(models.TextChoices):
    """
    Статусы назначенной роли пользователя.

    Роль может быть назначена, но ещё не подтверждена.
    Это важно для регистрации преподавателя, учащегося и родителя.
    """

    PENDING = "pending", "Ожидает подтверждения"
    ACTIVE = "active", "Активна"
    REJECTED = "rejected", "Отклонена"
    REVOKED = "revoked", "Отозвана"
    ARCHIVED = "archived", "В архиве"


class ProfileStatus(models.TextChoices):
    """
    Статусы ролевого профиля пользователя.

    Используется для:
        - LearnerProfile;
        - GuardianProfile;
        - TeacherProfile.
    """

    DRAFT = "draft", "Черновик"
    PENDING_REVIEW = "pending_review", "Ожидает проверки"
    VERIFIED = "verified", "Подтверждён"
    REJECTED = "rejected", "Отклонён"
    ARCHIVED = "archived", "В архиве"


class GuardianLearnerStatus(models.TextChoices):
    """
    Статусы связи между родителем и учащимся.
    """

    PENDING = "pending", "Ожидает подтверждения"
    ACTIVE = "active", "Активна"
    REJECTED = "rejected", "Отклонена"
    REVOKED = "revoked", "Отозвана"
    ARCHIVED = "archived", "В архиве"


ACTIVE_USER_STATUSES = {
    UserStatus.ACTIVE,
}
"""Статусы, при которых пользователь считается активным участником системы."""


INACTIVE_USER_STATUSES = {
    UserStatus.REJECTED,
    UserStatus.BLOCKED,
    UserStatus.ARCHIVED,
    UserStatus.SCHEDULED_FOR_DELETION,
    UserStatus.ANONYMIZED,
}
"""Статусы, при которых пользователь не должен иметь полноценный доступ к системе."""


DELETION_CANDIDATE_USER_STATUSES = {
    UserStatus.REJECTED,
    UserStatus.BLOCKED,
    UserStatus.ARCHIVED,
    UserStatus.SCHEDULED_FOR_DELETION,
}
"""Статусы, из которых пользователь может перейти к анонимизации."""


FINAL_USER_STATUSES = {
    UserStatus.ANONYMIZED,
}
"""Финальные статусы жизненного цикла пользователя."""


ACTIVE_ROLE_STATUSES = {
    UserRoleStatus.ACTIVE,
}
"""Статусы, при которых роль считается активной."""


INACTIVE_ROLE_STATUSES = {
    UserRoleStatus.PENDING,
    UserRoleStatus.REJECTED,
    UserRoleStatus.REVOKED,
    UserRoleStatus.ARCHIVED,
}
"""Статусы, при которых роль не должна давать доступ."""


VERIFIED_PROFILE_STATUSES = {
    ProfileStatus.VERIFIED,
}
"""Статусы, при которых профиль считается подтверждённым."""


ACTIVE_GUARDIAN_LEARNER_STATUSES = {
    GuardianLearnerStatus.ACTIVE,
}
"""Статусы, при которых связь родителя и учащегося считается активной."""
