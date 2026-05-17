from __future__ import annotations


class UserEmailSubject:
    """
    Темы писем приложения users.
    """

    EMAIL_VERIFICATION = "Подтверждение email в ЦОС «Пифагор»"
    TEACHER_REGISTRATION_PENDING = "Заявка преподавателя отправлена на проверку"
    LEARNER_PROFILE_REQUIRED = "Завершите настройку профиля учащегося"
    GUARDIAN_REGISTRATION_COMPLETED = "Регистрация родителя в ЦОС «Пифагор»"

    JOIN_REQUEST_APPROVED = "Ваша заявка в ЦОС «Пифагор» подтверждена"
    JOIN_REQUEST_REJECTED = "Ваша заявка в ЦОС «Пифагор» отклонена"
    JOIN_REQUEST_CREATED_FOR_REVIEWER = "Новая заявка ожидает проверки"

    GUARDIAN_LINK_REQUESTED = "Запрос на связь родителя и учащегося"
    GUARDIAN_LINK_APPROVED = "Связь родителя и учащегося подтверждена"

    ACCOUNT_BLOCKED = "Аккаунт в ЦОС «Пифагор» заблокирован"
    ACCOUNT_SCHEDULED_FOR_DELETION = "Аккаунт будет анонимизирован"

    PASSWORD_RESET = "Восстановление пароля в ЦОС «Пифагор»"
