from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationRole,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.services import build_deduplication_key, create_notification


def notify_learner_about_test_result(*, attempt) -> None:
    """
    Уведомляет обучающегося о публикации результата теста.
    """

    create_notification(
        recipient=attempt.learner,
        title="Результат теста опубликован",
        message=_build_learner_result_message(attempt=attempt),
        notification_type=NotificationType.SYSTEM,
        category=NotificationCategory.TESTS,
        level=NotificationLevel.SUCCESS,
        recipient_role=NotificationRole.LEARNER,
        source_type=NotificationSourceType.TEST,
        source_id=str(attempt.test_id),
        deduplication_key=_build_result_deduplication_key(
            user=attempt.learner,
            attempt=attempt,
            role="learner",
        ),
        action_label="Открыть результат",
        action_url=_build_learner_result_url(attempt=attempt),
        payload=_build_result_payload(
            attempt=attempt,
            role="learner",
        ),
    )


def notify_guardian_about_test_result(*, attempt) -> None:
    """
    Уведомляет родителей о публикации результата теста.
    """

    guardians = get_guardians_for_learner(learner=attempt.learner)

    for guardian in guardians:
        create_notification(
            recipient=guardian,
            title="Опубликована оценка ребёнка за тест",
            message=_build_guardian_result_message(attempt=attempt),
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.TESTS,
            level=NotificationLevel.INFO,
            recipient_role=NotificationRole.GUARDIAN,
            source_type=NotificationSourceType.TEST,
            source_id=str(attempt.test_id),
            deduplication_key=_build_result_deduplication_key(
                user=guardian,
                attempt=attempt,
                role="guardian",
            ),
            action_label="Открыть результат",
            action_url=_build_guardian_result_url(attempt=attempt),
            payload=_build_result_payload(
                attempt=attempt,
                role="guardian",
            ),
        )


def get_guardians_for_learner(*, learner) -> list:
    """
    Возвращает родителей обучающегося.

    Сделано мягко, чтобы testing не зависел жёстко от конкретной реализации
    guardian-связей в users/education.
    """

    guardians = []

    for relation_name in (
        "guardian_links",
        "parent_links",
        "learner_guardians",
        "guardian_relations",
    ):
        relation_manager = getattr(learner, relation_name, None)

        if relation_manager is None:
            continue

        guardians.extend(
            _extract_guardians_from_relation_manager(
                relation_manager=relation_manager,
            )
        )

    return _unique_users(users=guardians)


def _extract_guardians_from_relation_manager(*, relation_manager) -> list:
    """
    Достаёт пользователей-родителей из reverse relation manager.
    """

    guardians = []

    for relation in relation_manager.all():
        guardian = (
            getattr(relation, "guardian", None)
            or getattr(relation, "parent", None)
            or getattr(relation, "user", None)
            or getattr(relation, "guardian_user", None)
            or getattr(relation, "parent_user", None)
        )

        if guardian is not None:
            guardians.append(guardian)

    return guardians


def _unique_users(*, users: list) -> list:
    """
    Убирает дубли пользователей.
    """

    unique_users = []
    seen_ids = set()

    for user in users:
        user_id = getattr(user, "id", None)

        if user_id is None or user_id in seen_ids:
            continue

        seen_ids.add(user_id)
        unique_users.append(user)

    return unique_users


def _build_learner_result_message(*, attempt) -> str:
    """
    Формирует сообщение для обучающегося.
    """

    return (
        f"Преподаватель подтвердил результат теста "
        f"«{attempt.test.title}». Итоговая оценка: {attempt.final_grade}."
    )


def _build_guardian_result_message(*, attempt) -> str:
    """
    Формирует сообщение для родителя.
    """

    learner_name = _get_user_display_name(user=attempt.learner)

    return (
        f"Опубликован результат теста «{attempt.test.title}» "
        f"для обучающегося {learner_name}. "
        f"Итоговая оценка: {attempt.final_grade}."
    )


def _build_result_deduplication_key(
    *,
    user,
    attempt,
    role: str,
) -> str:
    """
    Формирует ключ дедупликации уведомления о результате.
    """

    return build_deduplication_key(
        user_id=user.id,
        notification_type=NotificationType.SYSTEM,
        source_type=NotificationSourceType.TEST,
        source_id=f"attempt:{attempt.id}:result:{role}",
    )


def _build_result_payload(
    *,
    attempt,
    role: str,
) -> dict:
    """
    Формирует payload уведомления.
    """

    return {
        "role": role,
        "test_id": attempt.test_id,
        "test_title": attempt.test.title,
        "attempt_id": attempt.id,
        "attempt_number": attempt.attempt_number,
        "learner_id": attempt.learner_id,
        "final_score": str(attempt.final_score),
        "final_grade": attempt.final_grade,
        "published_at": (
            attempt.published_at.isoformat() if attempt.published_at else None
        ),
    }


def _build_learner_result_url(*, attempt) -> str:
    """
    Возвращает ссылку на результат для обучающегося.
    """

    return f"/student/tests/{attempt.test_id}/attempts/{attempt.id}"


def _build_guardian_result_url(*, attempt) -> str:
    """
    Возвращает ссылку на результат для родителя.
    """

    return f"/parent/tests/{attempt.test_id}/attempts/{attempt.id}"


def _get_user_display_name(*, user) -> str:
    """
    Возвращает отображаемое имя пользователя.
    """

    full_name = ""

    if hasattr(user, "get_full_name"):
        full_name = user.get_full_name()

    if full_name:
        return full_name

    return getattr(user, "email", str(user))
