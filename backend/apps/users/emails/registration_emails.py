from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context
from apps.users.emails.email_subjects import UserEmailSubject
from apps.users.services.email_verification_services import build_email_verification_url
from apps.users.services.password_reset_services import build_password_reset_url


def send_email_verification_email(*, user) -> int:
    """
    Отправляет письмо подтверждения email.

    Args:
        user:
            Пользователь.

    Returns:
        int: Количество успешно отправленных писем.
    """

    verification_url = build_email_verification_url(user=user)

    context = get_base_email_context(
        user=user,
        title="Подтвердите email",
        preview_text="Добро пожаловать в ЦОС «Пифагор». Подтвердите email, чтобы завершить первый этап регистрации.",
        action_url=verification_url,
        action_label="Перейти к подтверждению",
        next_steps=[
            "Перейдите по ссылке подтверждения.",
            "Вернитесь на платформу.",
            "Завершите настройку профиля в зависимости от вашей роли.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.EMAIL_VERIFICATION,
        to_email=user.email,
        template_base="emails/users/registration/email_verification",
        context=context,
    )


def send_teacher_registration_pending_email(*, user) -> int:
    """
    Отправляет письмо преподавателю о том, что заявка отправлена на проверку.

    Args:
        user:
            Пользователь преподавателя.

    Returns:
        int: Количество успешно отправленных писем.
    """

    context = get_base_email_context(
        user=user,
        title="Заявка преподавателя отправлена администратору",
        preview_text="Ваша заявка преподавателя отправлена администратору образовательной организации.",
        action_url="/teacher",
        action_label="Посмотреть статус заявки",
        next_steps=[
            "Администратор образовательной организации рассмотрит заявку.",
            "После подтверждения вы получите доступ к рабочему пространству преподавателя.",
            "Если потребуется уточнение, с вами свяжутся дополнительно.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.TEACHER_REGISTRATION_PENDING,
        to_email=user.email,
        template_base="emails/users/registration/teacher_registration_pending",
        context=context,
    )


def send_learner_profile_required_email(*, user) -> int:
    """
    Отправляет письмо учащемуся с просьбой заполнить профиль.

    Args:
        user:
            Пользователь учащегося.

    Returns:
        int: Количество успешно отправленных писем.
    """

    context = get_base_email_context(
        user=user,
        title="Завершите настройку профиля учащегося",
        preview_text="Email подтверждён. Теперь нужно завершить настройку профиля учащегося.",
        action_url="/profile/setup",
        action_label="Продолжить настройку профиля",
        next_steps=[
            "Укажите образовательную организацию.",
            "Выберите группу или класс.",
            "Отправьте профиль на проверку куратору.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.LEARNER_PROFILE_REQUIRED,
        to_email=user.email,
        template_base="emails/users/registration/learner_profile_required",
        context=context,
    )


def send_guardian_registration_completed_email(*, user) -> int:
    """
    Отправляет письмо родителю после регистрации.

    Args:
        user:
            Пользователь родителя.

    Returns:
        int: Количество успешно отправленных писем.
    """

    context = get_base_email_context(
        user=user,
        title="Кабинет родителя готов к настройке",
        preview_text="Ваш кабинет родителя готов. Теперь можно добавить ребёнка или отправить заявку на связь.",
        action_url="/guardian/children",
        action_label="Перейти в кабинет родителя",
        next_steps=[
            "Перейдите в кабинет родителя.",
            "Добавьте ребёнка или отправьте заявку на связь.",
            "Дождитесь подтверждения куратора или администратора.",
        ],
    )

    return send_templated_email(
        subject=UserEmailSubject.GUARDIAN_REGISTRATION_COMPLETED,
        to_email=user.email,
        template_base="emails/users/registration/guardian_registration_completed",
        context=context,
    )


def send_password_reset_email(*, user) -> int:
    """
    Отправляет письмо восстановления пароля.

    Args:
        user:
            Пользователь.

    Returns:
        int: Количество успешно отправленных писем.
    """

    reset_url = build_password_reset_url(user=user)

    context = get_base_email_context(
        user=user,
        title="Восстановление пароля",
        preview_text="Мы получили запрос на восстановление пароля в ЦОС «Пифагор».",
        action_url=reset_url,
        action_label="Создать новый пароль",
        next_steps=[
            "Перейдите по ссылке восстановления.",
            "Создайте новый надёжный пароль.",
            "Вернитесь на платформу и войдите в аккаунт.",
        ],
        security_note=(
            "Если вы не запрашивали восстановление пароля, просто проигнорируйте это письмо. "
            "Ваш текущий пароль останется прежним."
        ),
    )

    return send_templated_email(
        subject=UserEmailSubject.PASSWORD_RESET,
        to_email=user.email,
        template_base="emails/users/registration/password_reset",
        context=context,
    )
