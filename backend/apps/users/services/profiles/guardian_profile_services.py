from __future__ import annotations

from apps.core.exceptions import ConflictApplicationError
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import GuardianLearner, GuardianProfile


def create_guardian_profile(
    *,
    user,
    status: str = ProfileStatus.DRAFT,
) -> GuardianProfile:
    """
    Создаёт профиль родителя или законного представителя.

    Args:
        user:
            Пользователь родителя.
        status:
            Статус профиля.

    Returns:
        GuardianProfile: Созданный профиль родителя.
    """

    return GuardianProfile.objects.create(
        user=user,
        status=status,
    )


def create_guardian_learner_link(
    *,
    guardian,
    learner,
    relation_type: str = GuardianLearner.RelationType.OTHER,
    is_primary: bool = False,
    is_learner_consent_required: bool = False,
    requested_by=None,
) -> GuardianLearner:
    """
    Создаёт связь родителя и учащегося.

    Args:
        guardian:
            Родитель или законный представитель.
        learner:
            Учащийся.
        relation_type:
            Тип связи.
        is_primary:
            Является ли представитель основным.
        is_learner_consent_required:
            Требуется ли согласие учащегося.
        requested_by:
            Инициатор запроса.

    Returns:
        GuardianLearner: Созданная связь родителя и учащегося.
    """

    if GuardianLearner.objects.filter(guardian=guardian, learner=learner).exists():
        raise ConflictApplicationError(
            "Связь родителя и учащегося уже существует.",
            code="guardian_learner_link_exists",
        )

    link = GuardianLearner.objects.create(
        guardian=guardian,
        learner=learner,
        relation_type=relation_type,
        is_primary=is_primary,
        is_learner_consent_required=is_learner_consent_required,
        requested_by=requested_by,
    )
    link.full_clean()
    link.save()

    return link
