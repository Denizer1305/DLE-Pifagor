from __future__ import annotations


class BackofficeUserMessage:
    """
    Человекочитаемые сообщения административного управления пользователями.
    """

    USER_NOT_FOUND_OR_FORBIDDEN = (
        "Пользователь не найден или недоступен для текущего администратора."
    )
    SELF_STATUS_CHANGE_FORBIDDEN = (
        "Администратор не может менять собственный статус "
        "через административное управление пользователями."
    )
    SELF_DELETE_FORBIDDEN = "Администратор не может запланировать удаление самого себя."
    FINAL_STATUS_FORBIDDEN = "Нельзя изменить статус анонимизированного пользователя."
    USER_ALREADY_BLOCKED = "Пользователь уже заблокирован."
    USER_ALREADY_ACTIVE = "Пользователь уже активен."
    USER_ALREADY_ARCHIVED = "Пользователь уже находится в архиве."
    USER_ALREADY_SCHEDULED_FOR_DELETION = (
        "Пользователь уже запланирован к удалению. "
        "Сначала восстановите пользователя."
    )
    UNSUPPORTED_BULK_ACTION = "Неподдерживаемое массовое действие."
    EMPTY_BULK_USER_IDS = "Необходимо выбрать хотя бы одного пользователя."
    STALE_OBJECT = (
        "Пользователь уже был изменён другим администратором. "
        "Обновите страницу и повторите действие."
    )
    UPDATE_PAYLOAD_EMPTY = "Необходимо передать хотя бы одно поле для изменения."
    ROLE_PAYLOAD_REQUIRED = (
        "Для массового изменения ролей необходимо передать role_payload."
    )
    ROLE_PAYLOAD_FORBIDDEN = (
        "role_payload можно передавать только для действия change_roles."
    )
    ROLE_NOT_FOUND = "Роль не найдена."
    ROLE_NOT_AVAILABLE = "Эта роль недоступна для назначения."
    ROLE_ASSIGNMENT_FORBIDDEN = "Недостаточно прав для назначения роли."
    ROLE_REVOKE_FORBIDDEN = "Недостаточно прав для отзыва роли."
