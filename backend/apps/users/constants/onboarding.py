from django.db import models


class JoinRequestType(models.TextChoices):
    """
    Типы заявок на присоединение пользователя.

    Заявка используется для подтверждения:
        - преподавателя в образовательную организацию;
        - учащегося в группу;
        - родителя к учащемуся.
    """

    TEACHER_TO_ORGANIZATION = (
        "teacher_to_organization",
        "Преподаватель в организацию",
    )
    LEARNER_TO_GROUP = (
        "learner_to_group",
        "Учащийся в группу",
    )
    GUARDIAN_TO_LEARNER = (
        "guardian_to_learner",
        "Родитель к учащемуся",
    )


class JoinRequestStatus(models.TextChoices):
    """
    Статусы заявки на присоединение.
    """

    PENDING = "pending", "Ожидает проверки"
    APPROVED = "approved", "Подтверждена"
    REJECTED = "rejected", "Отклонена"
    CANCELLED = "cancelled", "Отменена"
    EXPIRED = "expired", "Истекла"


class InviteCodePurpose(models.TextChoices):
    """
    Назначение временного кода приглашения.

    Коды используются для регистрации сотрудников и подтверждения
    родительской связи.
    """

    TEACHER_REGISTRATION = (
        "teacher_registration",
        "Регистрация преподавателя",
    )
    GUARDIAN_LINK_CURATOR = (
        "guardian_link_curator",
        "Связь родителя: код куратора",
    )
    GUARDIAN_LINK_LEARNER = (
        "guardian_link_learner",
        "Связь родителя: код учащегося",
    )


class RegistrationAttemptStatus(models.TextChoices):
    """
    Статусы попытки регистрации.

    Используются для аудита и ограничения количества запросов.
    """

    SUCCESS = "success", "Успешно"
    FAILED = "failed", "Ошибка"
    BLOCKED = "blocked", "Заблокировано лимитом"


class RegistrationFailureReason(models.TextChoices):
    """
    Причины неудачной попытки регистрации.

    Используется в RegistrationAttemptLog.
    """

    INVALID_INVITE_CODE = "invalid_invite_code", "Неверный код приглашения"
    EXPIRED_INVITE_CODE = "expired_invite_code", "Срок действия кода истёк"
    USED_INVITE_CODE = "used_invite_code", "Код уже использован"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded", "Превышен лимит попыток"
    INVALID_ROLE = "invalid_role", "Недопустимая роль"
    EMAIL_ALREADY_EXISTS = "email_already_exists", "Email уже используется"
    PHONE_ALREADY_EXISTS = "phone_already_exists", "Телефон уже используется"
    VALIDATION_ERROR = "validation_error", "Ошибка проверки данных"
    UNKNOWN_ERROR = "unknown_error", "Неизвестная ошибка"


PENDING_JOIN_REQUEST_STATUSES = {
    JoinRequestStatus.PENDING,
}
"""Статусы заявок, которые ожидают рассмотрения."""


FINAL_JOIN_REQUEST_STATUSES = {
    JoinRequestStatus.APPROVED,
    JoinRequestStatus.REJECTED,
    JoinRequestStatus.CANCELLED,
    JoinRequestStatus.EXPIRED,
}
"""Финальные статусы заявок."""


ACTIVE_INVITE_CODE_PURPOSES = {
    InviteCodePurpose.TEACHER_REGISTRATION,
    InviteCodePurpose.GUARDIAN_LINK_CURATOR,
    InviteCodePurpose.GUARDIAN_LINK_LEARNER,
}
"""Активные назначение кодов приглашения."""


GUARDIAN_LINK_INVITE_CODE_PURPOSES = {
    InviteCodePurpose.GUARDIAN_LINK_CURATOR,
    InviteCodePurpose.GUARDIAN_LINK_LEARNER,
}
"""Коды, используемые для подтверждения связи родителя и учащегося."""


DEFAULT_INVITE_CODE_LENGTH = 10
"""Стандартная длина кода приглашения."""


DEFAULT_INVITE_CODE_TTL_HOURS = 72
"""Стандартное время жизни кода приглашения в часах."""


DEFAULT_GUARDIAN_LINK_CODE_TTL_HOURS = 24
"""Стандартное время жизни кода связи родителя и учащегося."""


REGISTRATION_ATTEMPT_LIMIT = 5
"""Количество допустимых неудачных попыток регистрации."""


REGISTRATION_ATTEMPT_WINDOW_MINUTES = 15
"""Период в минутах, за который считается лимит попыток регистрации."""
