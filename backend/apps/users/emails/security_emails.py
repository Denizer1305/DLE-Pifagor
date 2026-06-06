from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context
from apps.users.emails.email_subjects import UserEmailSubject


def send_password_changed_email(*, user) -> int:
    context = get_base_email_context(
        user=user,
        title="Пароль изменён",
        preview_text="Пароль вашего аккаунта в ЦОС «Пифагор» был изменён.",
        action_url="/settings/security",
        action_label="Открыть безопасность",
        next_steps=[
            "Если это сделали вы, дополнительных действий не требуется.",
            "Если вы не меняли пароль, восстановите доступ и обратитесь в поддержку.",
        ],
        security_note=(
            "Это защитное уведомление. Оно помогает быстро заметить изменения "
            "доступа к аккаунту."
        ),
    )

    return send_templated_email(
        subject=UserEmailSubject.PASSWORD_CHANGED,
        to_email=user.email,
        template_base="emails/users/security/password_changed",
        context=context,
    )


def send_account_contact_changed_email(
    *,
    user,
    changed_fields: list[str] | None = None,
) -> int:
    context = get_base_email_context(
        user=user,
        title="Контактные данные изменены",
        preview_text="В вашем аккаунте ЦОС «Пифагор» изменились контактные данные.",
        action_url="/settings/security",
        action_label="Проверить настройки",
        next_steps=[
            "Проверьте актуальность email, телефона и резервных контактов.",
            "Если изменения внесли не вы, срочно смените пароль.",
        ],
        security_note=(
            "Если вы не выполняли это действие, обратитесь в образовательную "
            "организацию или службу поддержки."
        ),
        extra_context={
            "changed_fields": changed_fields or [],
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.ACCOUNT_CONTACT_CHANGED,
        to_email=user.email,
        template_base="emails/users/security/contact_changed",
        context=context,
    )


def send_user_roles_changed_email(
    *,
    user,
    assigned_roles: list[str] | None = None,
    revoked_roles: list[str] | None = None,
) -> int:
    context = get_base_email_context(
        user=user,
        title="Роли пользователя изменены",
        preview_text="Для вашего аккаунта в ЦОС «Пифагор» изменили роли доступа.",
        action_url="/profile",
        action_label="Открыть профиль",
        next_steps=[
            "Проверьте доступные разделы личного кабинета.",
            "Если роль назначена ошибочно, обратитесь к администратору организации.",
        ],
        extra_context={
            "assigned_roles": assigned_roles or [],
            "revoked_roles": revoked_roles or [],
        },
    )

    return send_templated_email(
        subject=UserEmailSubject.USER_ROLES_CHANGED,
        to_email=user.email,
        template_base="emails/users/security/roles_changed",
        context=context,
    )
