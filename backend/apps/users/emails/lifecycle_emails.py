from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context
from apps.users.emails.email_subjects import UserEmailSubject


def send_account_blocked_email(*, user, reason: str = "") -> int:
    """
    Отправляет письмо о блокировке аккаунта.
    """

    context = get_base_email_context(
        user=user,
        title="Аккаунт временно заблокирован",
        preview_text="Ваш аккаунт в ЦОС «Пифагор» временно заблокирован.",
        next_steps=[
            "Не создавайте повторный аккаунт до уточнения ситуации.",
            "Обратитесь в образовательную организацию.",
            "Дождитесь ответа ответственного сотрудника.",
        ],
        extra_context={
            "reason": reason,
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_BLOCKED,
        to_email=user.email,
        template_base="emails/users/lifecycle/account_blocked",
        context=context,
    )


def send_account_scheduled_for_deletion_email(
    *,
    user,
    scheduled_for_deletion_at=None,
) -> int:
    """
    Отправляет письмо о запланированной анонимизации аккаунта.
    """

    context = get_base_email_context(
        user=user,
        title="Аккаунт будет анонимизирован",
        preview_text="Аккаунт переведён в состояние ожидания анонимизации.",
        action_url="/support",
        action_label="Связаться с организацией",
        next_steps=[
            "Если вы считаете, что произошла ошибка, обратитесь в образовательную организацию.",
            "Не создавайте повторный аккаунт до уточнения ситуации.",
            "Дождитесь ответа ответственного сотрудника.",
        ],
        extra_context={
            "scheduled_for_deletion_at": scheduled_for_deletion_at,
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_SCHEDULED_FOR_DELETION,
        to_email=user.email,
        template_base="emails/users/lifecycle/scheduled_for_deletion",
        context=context,
    )


def send_account_anonymized_email(*, user) -> int:
    """
    Отправляет письмо об анонимизации аккаунта.
    """

    context = get_base_email_context(
        user=user,
        title="Аккаунт анонимизирован",
        preview_text="Аккаунт в ЦОС «Пифагор» был анонимизирован.",
        security_note="Это информационное письмо. Если у вас есть вопросы, обратитесь в образовательную организацию или службу поддержки.",
    )

    return send_templated_email(
        subject="Аккаунт в ЦОС «Пифагор» анонимизирован",
        to_email=user.email,
        template_base="emails/users/lifecycle/account_anonymized",
        context=context,
    )
