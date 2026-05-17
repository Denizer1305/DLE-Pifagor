from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context
from apps.users.emails.email_subjects import UserEmailSubject


def send_guardian_link_requested_email(*, user) -> int:
    """
    Отправляет письмо о создании запроса связи родителя и учащегося.
    """

    context = get_base_email_context(
        user=user,
        title="Запрос на связь родителя и учащегося",
        preview_text="В ЦОС «Пифагор» создан запрос на связь родителя и учащегося.",
        action_url="/guardian/children",
        action_label="Открыть кабинет родителя",
        next_steps=[
            "Дождитесь проверки запроса.",
            "Следите за статусом связи в кабинете родителя.",
            "Если данные указаны неверно, обратитесь к куратору или администратору.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.GUARDIAN_LINK_REQUESTED,
        to_email=user.email,
        template_base="emails/users/guardian/link_requested",
        context=context,
    )


def send_guardian_link_approved_email(*, user) -> int:
    """
    Отправляет письмо о подтверждении связи родителя и учащегося.
    """

    context = get_base_email_context(
        user=user,
        title="Связь родителя и учащегося подтверждена",
        preview_text="Связь родителя и учащегося подтверждена.",
        action_url="/guardian/children",
        action_label="Открыть кабинет родителя",
        next_steps=[
            "Перейдите в кабинет родителя.",
            "Откройте профиль ребёнка.",
            "Следите за важными учебными событиями и уведомлениями.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.GUARDIAN_LINK_APPROVED,
        to_email=user.email,
        template_base="emails/users/guardian/link_approved",
        context=context,
    )


def send_guardian_link_rejected_email(*, user, review_comment: str = "") -> int:
    """
    Отправляет письмо об отклонении связи родителя и учащегося.
    """

    context = get_base_email_context(
        user=user,
        title="Связь не была подтверждена",
        preview_text="Запрос на связь родителя и учащегося не был подтверждён.",
        action_url="/guardian/children",
        action_label="Посмотреть статус",
        next_steps=[
            "Проверьте введённые данные.",
            "При необходимости обратитесь к куратору или ответственному сотруднику.",
            "Повторите запрос после уточнения данных, если это доступно.",
        ],
        extra_context={
            "review_comment": review_comment,
        },
    )

    return send_templated_email(
        subject="Связь родителя и учащегося не подтверждена",
        to_email=user.email,
        template_base="emails/users/guardian/link_rejected",
        context=context,
    )
