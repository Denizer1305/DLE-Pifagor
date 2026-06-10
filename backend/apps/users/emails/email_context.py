from __future__ import annotations

from django.conf import settings


def get_user_greeting(user) -> str:
    """
    Формирует обращение к пользователю.

    Если известны имя и отчество, используется обращение по имени и отчеству.
    Если отчества нет, используется имя.
    Если имени нет, используется нейтральное обращение.

    Args:
        user:
            Пользователь.

    Returns:
        str: Обращение для письма.
    """

    if not user:
        return "Здравствуйте!"

    first_name = getattr(user, "first_name", "") or ""
    middle_name = getattr(user, "middle_name", "") or ""

    if first_name and middle_name:
        return f"Здравствуйте, {first_name} {middle_name}!"

    if first_name:
        return f"Здравствуйте, {first_name}!"

    return "Здравствуйте!"


def build_frontend_url(path: str = "") -> str:
    """
    Формирует абсолютную ссылку на frontend.

    Args:
        path:
            Путь внутри frontend-приложения.

    Returns:
        str: Абсолютная ссылка.
    """

    base_url = getattr(settings, "FRONTEND_BASE_URL", "https://edu-pifagor.ru")

    if not path:
        return base_url.rstrip("/")

    if path.startswith("http://") or path.startswith("https://"):
        return path

    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def get_email_logo_url() -> str:
    logo_url = getattr(settings, "EMAIL_LOGO_URL", "") or getattr(
        settings,
        "PIFAGOR_EMAIL_LOGO_URL",
        "",
    )

    if logo_url:
        return logo_url

    return build_frontend_url("/email/logo-pifagor.png")


def get_support_email() -> str:
    return getattr(settings, "SUPPORT_EMAIL", "") or getattr(
        settings,
        "PIFAGOR_SUPPORT_EMAIL",
        "",
    )


def get_base_email_context(
    *,
    user=None,
    title: str = "",
    preview_text: str = "",
    action_url: str = "",
    action_label: str = "",
    next_steps: list[str] | None = None,
    security_note: str = "",
    extra_context: dict | None = None,
) -> dict:
    """
    Формирует базовый контекст для email-шаблонов.

    Args:
        user:
            Получатель письма.
        title:
            Заголовок письма.
        preview_text:
            Короткий текст предпросмотра.
        action_url:
            Ссылка основного действия.
        action_label:
            Текст кнопки основного действия.
        next_steps:
            Список шагов блока "Что дальше?".
        security_note:
            Текст блока безопасности.
        extra_context:
            Дополнительный контекст письма.

    Returns:
        dict: Контекст письма.
    """

    context = {
        "project_name": "ЦОС «Пифагор»",
        "platform_name": "Цифровая образовательная среда «Пифагор»",
        "title": title,
        "preview_text": preview_text,
        "greeting": get_user_greeting(user),
        "user": user,
        "action_url": build_frontend_url(action_url) if action_url else "",
        "action_label": action_label,
        "next_steps": next_steps or [],
        "security_note": security_note
        or "Если вы не выполняли это действие, не переходите по ссылкам из письма и обратитесь в образовательную организацию или службу поддержки.",
        "support_email": get_support_email(),
        "logo_url": get_email_logo_url(),
        "signature": "С уважением, команда ЦОС «Пифагор»",
    }

    if extra_context:
        context.update(extra_context)

    return context
