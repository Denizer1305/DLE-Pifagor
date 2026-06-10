from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context
from apps.users.emails.email_subjects import UserEmailSubject


def send_account_blocked_email(*, user, reason: str = "") -> int:
    context = get_base_email_context(
        user=user,
        title="Аккаунт временно заблокирован",
        preview_text="Ваш аккаунт в ЦОС «Пифагор» временно заблокирован.",
        next_steps=[
            "Не создавайте повторный аккаунт до уточнения ситуации.",
            "Обратитесь в образовательную организацию.",
            "Дождитесь ответа ответственного сотрудника.",
        ],
        extra_context={"reason": reason},
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_BLOCKED,
        to_email=user.email,
        template_base="emails/users/lifecycle/account_blocked",
        context=context,
    )


def send_account_unblocked_email(*, user, reason: str = "") -> int:
    context = get_base_email_context(
        user=user,
        title="Аккаунт разблокирован",
        preview_text="Ваш аккаунт в ЦОС «Пифагор» снова доступен.",
        action_url="/dashboard",
        action_label="Перейти в кабинет",
        next_steps=[
            "Войдите в личный кабинет.",
            "Проверьте профиль и доступные разделы.",
            "Если доступ работает некорректно, обратитесь к администратору.",
        ],
        extra_context={"reason": reason},
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_UNBLOCKED,
        to_email=user.email,
        template_base="emails/users/lifecycle/account_unblocked",
        context=context,
    )


def send_account_archived_email(*, user, reason: str = "") -> int:
    context = get_base_email_context(
        user=user,
        title="Аккаунт архивирован",
        preview_text="Ваш аккаунт в ЦОС «Пифагор» был переведён в архив.",
        action_url="/support",
        action_label="Связаться с организацией",
        next_steps=[
            "Если вы считаете архивирование ошибкой, обратитесь в организацию.",
            "Не создавайте повторный аккаунт до уточнения ситуации.",
        ],
        extra_context={"reason": reason},
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_ARCHIVED,
        to_email=user.email,
        template_base="emails/users/lifecycle/account_archived",
        context=context,
    )


def send_account_restored_email(
    *,
    user,
    previous_status: str = "",
    reason: str = "",
) -> int:
    context = get_base_email_context(
        user=user,
        title="Аккаунт восстановлен",
        preview_text="Ваш аккаунт в ЦОС «Пифагор» был восстановлен.",
        action_url="/dashboard",
        action_label="Перейти в кабинет",
        next_steps=[
            "Войдите в личный кабинет.",
            "Проверьте профиль, роли и уведомления.",
            "Если часть доступа не восстановилась, обратитесь к администратору.",
        ],
        extra_context={
            "previous_status": previous_status,
            "reason": reason,
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_RESTORED,
        to_email=user.email,
        template_base="emails/users/lifecycle/account_restored",
        context=context,
    )


def send_account_scheduled_for_deletion_email(
    *,
    user,
    scheduled_for_deletion_at=None,
) -> int:
    context = get_base_email_context(
        user=user,
        title="Аккаунт будет анонимизирован",
        preview_text="Аккаунт переведён в состояние ожидания анонимизации.",
        action_url="/support",
        action_label="Связаться с организацией",
        next_steps=[
            "Если вы считаете, что произошла ошибка, обратитесь в организацию.",
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
    context = get_base_email_context(
        user=user,
        title="Аккаунт анонимизирован",
        preview_text="Аккаунт в ЦОС «Пифагор» был анонимизирован.",
        security_note=(
            "Это информационное письмо. Если у вас есть вопросы, обратитесь "
            "в образовательную организацию или службу поддержки."
        ),
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_ANONYMIZED,
        to_email=user.email,
        template_base="emails/users/lifecycle/account_anonymized",
        context=context,
    )
