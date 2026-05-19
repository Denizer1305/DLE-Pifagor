"""
Права доступа приложения feedback.

Публичная форма обратной связи использует AllowAny,
так как обращения могут отправлять незарегистрированные пользователи.

Для будущего административного API здесь можно добавить:
    - IsFeedbackManager;
    - IsSupportStaff;
    - CanManageFeedbackRequests.
"""

__all__: list[str] = []