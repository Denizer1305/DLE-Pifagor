from django.db import models


class UserAuditAction(models.TextChoices):
    """
    Типы действий для аудита пользователей.

    Аудит нужен, чтобы фиксировать важные действия:
        - регистрацию;
        - подтверждение email;
        - назначение роли;
        - создание заявки;
        - подтверждение заявки;
        - отклонение заявки;
        - блокировку;
        - архивацию;
        - анонимизацию.
    """

    USER_REGISTERED = "user_registered", "Пользователь зарегистрирован"
    EMAIL_VERIFIED = "email_verified", "Email подтверждён"
    PHONE_VERIFICATION_REQUESTED = (
        "phone_verification_requested",
        "Запрошено подтверждение телефона",
    )
    PHONE_VERIFIED = "phone_verified", "Телефон подтверждён"

    ROLE_ASSIGNED = "role_assigned", "Роль назначена"
    ROLE_APPROVED = "role_approved", "Роль подтверждена"
    ROLE_REJECTED = "role_rejected", "Роль отклонена"
    ROLE_REVOKED = "role_revoked", "Роль отозвана"

    JOIN_REQUEST_CREATED = "join_request_created", "Заявка создана"
    JOIN_REQUEST_APPROVED = "join_request_approved", "Заявка подтверждена"
    JOIN_REQUEST_REJECTED = "join_request_rejected", "Заявка отклонена"
    JOIN_REQUEST_CANCELLED = "join_request_cancelled", "Заявка отменена"
    JOIN_REQUEST_EXPIRED = "join_request_expired", "Заявка истекла"

    INVITE_CODE_CREATED = "invite_code_created", "Код приглашения создан"
    INVITE_CODE_USED = "invite_code_used", "Код приглашения использован"
    INVITE_CODE_EXPIRED = "invite_code_expired", "Код приглашения истёк"
    INVITE_CODE_DISABLED = "invite_code_disabled", "Код приглашения отключён"

    PROFILE_CREATED = "profile_created", "Профиль создан"
    PROFILE_UPDATED = "profile_updated", "Профиль обновлён"
    PROFILE_VERIFIED = "profile_verified", "Профиль подтверждён"
    PROFILE_REJECTED = "profile_rejected", "Профиль отклонён"

    AVATAR_SUBMITTED = "avatar_submitted", "Аватар отправлен на модерацию"
    AVATAR_APPROVED = "avatar_approved", "Аватар одобрен"
    AVATAR_REJECTED = "avatar_rejected", "Аватар отклонён"

    GUARDIAN_LINK_CREATED = (
        "guardian_link_created",
        "Связь родителя и учащегося создана",
    )
    GUARDIAN_LINK_APPROVED = (
        "guardian_link_approved",
        "Связь родителя и учащегося подтверждена",
    )
    GUARDIAN_LINK_REJECTED = (
        "guardian_link_rejected",
        "Связь родителя и учащегося отклонена",
    )
    GUARDIAN_LINK_REVOKED = (
        "guardian_link_revoked",
        "Связь родителя и учащегося отозвана",
    )

    USER_BLOCKED = "user_blocked", "Пользователь заблокирован"
    USER_UNBLOCKED = "user_unblocked", "Пользователь разблокирован"
    USER_ARCHIVED = "user_archived", "Пользователь архивирован"
    USER_RESTORED = "user_restored", "Пользователь восстановлен"
    USER_SCHEDULED_FOR_DELETION = (
        "user_scheduled_for_deletion",
        "Пользователь запланирован к удалению",
    )
    USER_ANONYMIZED = "user_anonymized", "Пользователь анонимизирован"

    LOGIN_SUCCESS = "login_success", "Успешный вход"
    LOGIN_FAILED = "login_failed", "Неудачная попытка входа"
    LOGOUT = "logout", "Выход из системы"


class AuditActorType(models.TextChoices):
    """
    Типы инициатора действия в аудите.
    """

    USER = "user", "Пользователь"
    SYSTEM = "system", "Система"
    ADMIN = "admin", "Администратор"


class AuditObjectType(models.TextChoices):
    """
    Типы объектов, с которыми связано действие аудита.

    Используется в metadata или будущей расширенной модели аудита.
    """

    USER = "user", "Пользователь"
    ROLE = "role", "Роль"
    USER_ROLE = "user_role", "Роль пользователя"
    PROFILE = "profile", "Профиль"
    LEARNER_PROFILE = "learner_profile", "Профиль учащегося"
    GUARDIAN_PROFILE = "guardian_profile", "Профиль родителя"
    TEACHER_PROFILE = "teacher_profile", "Профиль преподавателя"
    GUARDIAN_LEARNER = "guardian_learner", "Связь родителя и учащегося"
    INVITE_CODE = "invite_code", "Код приглашения"
    JOIN_REQUEST = "join_request", "Заявка"


SECURITY_AUDIT_ACTIONS = {
    UserAuditAction.LOGIN_SUCCESS,
    UserAuditAction.LOGIN_FAILED,
    UserAuditAction.LOGOUT,
    UserAuditAction.INVITE_CODE_USED,
    UserAuditAction.USER_BLOCKED,
    UserAuditAction.USER_ANONYMIZED,
}
"""Действия аудита, связанные с безопасностью."""


LIFECYCLE_AUDIT_ACTIONS = {
    UserAuditAction.USER_BLOCKED,
    UserAuditAction.USER_UNBLOCKED,
    UserAuditAction.USER_ARCHIVED,
    UserAuditAction.USER_RESTORED,
    UserAuditAction.USER_SCHEDULED_FOR_DELETION,
    UserAuditAction.USER_ANONYMIZED,
}
"""Действия аудита, связанные с жизненным циклом аккаунта."""


JOIN_REQUEST_AUDIT_ACTIONS = {
    UserAuditAction.JOIN_REQUEST_CREATED,
    UserAuditAction.JOIN_REQUEST_APPROVED,
    UserAuditAction.JOIN_REQUEST_REJECTED,
    UserAuditAction.JOIN_REQUEST_CANCELLED,
    UserAuditAction.JOIN_REQUEST_EXPIRED,
}
"""Действия аудита, связанные с заявками."""
