from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context
from apps.users.emails.email_subjects import UserEmailSubject


def send_join_request_approved_email(*, user) -> int:
    """
    Отправляет письмо о подтверждении заявки.
    """

    context = get_base_email_context(
        user=user,
        title="Ваша заявка подтверждена",
        preview_text="Ваша заявка в ЦОС «Пифагор» подтверждена.",
        action_url="/dashboard",
        action_label="Перейти в личный кабинет",
        next_steps=[
            "Перейдите в личный кабинет.",
            "Проверьте данные профиля.",
            "Начните пользоваться доступными разделами платформы.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.JOIN_REQUEST_APPROVED,
        to_email=user.email,
        template_base="emails/users/join_requests/approved",
        context=context,
    )


def send_join_request_rejected_email(*, user, review_comment: str = "") -> int:
    """
    Отправляет письмо об отклонении заявки.
    """

    context = get_base_email_context(
        user=user,
        title="Заявка не была подтверждена",
        preview_text="Ваша заявка в ЦОС «Пифагор» не была подтверждена.",
        action_url="/profile",
        action_label="Посмотреть подробности",
        next_steps=[
            "Проверьте введённые данные.",
            "При необходимости обратитесь в образовательную организацию.",
            "После уточнения данных повторите действие, если оно доступно.",
        ],
        extra_context={
            "review_comment": review_comment,
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.JOIN_REQUEST_REJECTED,
        to_email=user.email,
        template_base="emails/users/join_requests/rejected",
        context=context,
    )


def send_join_request_created_for_reviewer_email(
    *,
    reviewer,
    applicant_name: str = "",
    action_url: str = "/join-requests",
) -> int:
    """
    Отправляет проверяющему письмо о новой заявке.
    """

    context = get_base_email_context(
        user=reviewer,
        title="Новая заявка ожидает проверки",
        preview_text="В ЦОС «Пифагор» появилась новая заявка, ожидающая вашей проверки.",
        action_url=action_url,
        action_label="Открыть заявку",
        next_steps=[
            "Откройте раздел заявок.",
            "Проверьте данные пользователя.",
            "Подтвердите или отклоните заявку с понятным комментарием.",
        ],
        extra_context={
            "applicant_name": applicant_name,
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.JOIN_REQUEST_CREATED_FOR_REVIEWER,
        to_email=reviewer.email,
        template_base="emails/users/join_requests/created_for_reviewer",
        context=context,
    )
