from __future__ import annotations


class UserEmailSubject:
    """
    Темы писем приложения users.
    """

    EMAIL_VERIFICATION = "Подтверждение email в ЦОС «Пифагор»"
    TEACHER_REGISTRATION_PENDING = (
        "Заявка преподавателя отправлена на проверку"
    )
    LEARNER_PROFILE_REQUIRED = "Завершите настройку профиля учащегося"
    GUARDIAN_REGISTRATION_COMPLETED = "Регистрация родителя в ЦОС «Пифагор»"

    JOIN_REQUEST_APPROVED = "Ваша заявка в ЦОС «Пифагор» подтверждена"
    JOIN_REQUEST_REJECTED = "Ваша заявка в ЦОС «Пифагор» отклонена"
    JOIN_REQUEST_CREATED_FOR_REVIEWER = "Новая заявка ожидает проверки"

    GUARDIAN_LINK_REQUESTED = "Запрос на связь родителя и учащегося"
    GUARDIAN_LINK_APPROVED = "Связь родителя и учащегося подтверждена"
    GUARDIAN_LINK_REJECTED = "Связь родителя и учащегося не подтверждена"

    ACCOUNT_BLOCKED = "Аккаунт в ЦОС «Пифагор» заблокирован"
    ACCOUNT_UNBLOCKED = "Аккаунт в ЦОС «Пифагор» разблокирован"
    ACCOUNT_ARCHIVED = "Аккаунт в ЦОС «Пифагор» архивирован"
    ACCOUNT_RESTORED = "Аккаунт в ЦОС «Пифагор» восстановлен"
    ACCOUNT_SCHEDULED_FOR_DELETION = "Аккаунт будет анонимизирован"
    ACCOUNT_ANONYMIZED = "Аккаунт в ЦОС «Пифагор» анонимизирован"

    PASSWORD_RESET = "Восстановление пароля в ЦОС «Пифагор»"
    PASSWORD_CHANGED = "Пароль в ЦОС «Пифагор» изменён"
    ACCOUNT_CONTACT_CHANGED = "Контактные данные аккаунта изменены"
    USER_ROLES_CHANGED = "Роли в ЦОС «Пифагор» изменены"
