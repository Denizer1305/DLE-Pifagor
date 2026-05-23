from __future__ import annotations


def get_quick_actions_payload() -> list[dict]:
    """
    Возвращает быстрые действия администратора.
    """

    return [
        {
            "key": "create_user",
            "label": "Создать пользователя",
            "description": "Добавить новый аккаунт вручную",
            "icon": "fas fa-user-plus",
            "route_name": "admin-users-create",
            "tone": "primary",
        },
        {
            "key": "review_requests",
            "label": "Проверить заявки",
            "description": "Рассмотреть новые заявки на присоединение",
            "icon": "fas fa-user-check",
            "route_name": "admin-join-requests",
            "tone": "warning",
        },
        {
            "key": "feedback",
            "label": "Открыть обращения",
            "description": "Ответить пользователям и закрыть обращения",
            "icon": "fas fa-envelope-open-text",
            "route_name": "admin-feedback",
            "tone": "primary",
        },
        {
            "key": "create_course",
            "label": "Создать курс",
            "description": "Перейти к созданию учебного курса",
            "icon": "fas fa-book-medical",
            "route_name": "admin-courses-create",
            "tone": "success",
        },
    ]
