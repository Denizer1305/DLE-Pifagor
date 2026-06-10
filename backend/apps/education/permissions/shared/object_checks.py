from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.education.models import Curriculum, CurriculumItem, GroupSubject
from apps.education.selectors import (
    get_user_available_group_ids,
    get_user_available_organization_ids,
    user_is_global_admin,
)
from apps.organizations.models import StudyGroup
from django.contrib.auth import get_user_model

User = get_user_model()


def user_can_access_organization(
    *,
    user: User,
    organization_id: int | None,
) -> bool:
    """
    Проверяет доступ пользователя к организации.
    """

    if not organization_id:
        return False

    if user_is_global_admin(user):
        return True

    return organization_id in get_user_available_organization_ids(user)


def user_can_access_group(
    *,
    user: User,
    group_id: int | None,
) -> bool:
    """
    Проверяет доступ пользователя к учебной группе.
    """

    if not group_id:
        return False

    if user_is_global_admin(user):
        return True

    return group_id in get_user_available_group_ids(user)


def user_can_access_object_by_organization(
    *,
    user: User,
    obj: Any,
) -> bool:
    """
    Проверяет чтение объекта по организации.
    """

    organization_id = get_object_organization_id(obj)

    return user_can_access_organization(
        user=user,
        organization_id=organization_id,
    )


def user_can_access_object_by_group(
    *,
    user: User,
    obj: Any,
) -> bool:
    """
    Проверяет чтение объекта по учебной группе.
    """

    group_id = get_object_group_id(obj)

    return user_can_access_group(
        user=user,
        group_id=group_id,
    )


def user_can_manage_object_by_organization(
    *,
    user: User,
    obj: Any,
) -> bool:
    """
    Проверяет изменение объекта по организации.

    Сама проверка роли выполняется в permission-классе.
    Здесь проверяется только область доступа.
    """

    return user_can_access_object_by_organization(
        user=user,
        obj=obj,
    )


def user_can_manage_object_by_group(
    *,
    user: User,
    obj: Any,
) -> bool:
    """
    Проверяет изменение объекта по учебной группе.

    Сама проверка роли выполняется в permission-классе.
    Здесь проверяется только область доступа.
    """

    return user_can_access_object_by_group(
        user=user,
        obj=obj,
    )


def user_can_access_teacher_assignment(
    *,
    user: User,
    obj: Any,
) -> bool:
    """
    Проверяет доступ преподавателя к своему назначению.
    """

    teacher_id = get_object_teacher_id(obj)

    return bool(teacher_id and teacher_id == user.id)


def user_can_access_learner_enrollment(
    *,
    user: User,
    obj: Any,
) -> bool:
    """
    Проверяет доступ обучающегося к своему зачислению.
    """

    learner_id = get_object_learner_id(obj)

    return bool(learner_id and learner_id == user.id)


def get_object_organization_id(obj: Any) -> int | None:
    """
    Возвращает id организации для академического объекта.
    """

    direct_organization_id = getattr(obj, "organization_id", None)

    if direct_organization_id:
        return direct_organization_id

    curriculum = getattr(obj, "curriculum", None)

    if curriculum is not None:
        return getattr(curriculum, "organization_id", None)

    group = getattr(obj, "group", None)

    if group is not None:
        return getattr(group, "organization_id", None)

    group_subject = getattr(obj, "group_subject", None)

    if group_subject is not None:
        group_subject_group = getattr(group_subject, "group", None)

        if group_subject_group is not None:
            return getattr(group_subject_group, "organization_id", None)

    return None


def get_object_group_id(obj: Any) -> int | None:
    """
    Возвращает id учебной группы для академического объекта.
    """

    direct_group_id = getattr(obj, "group_id", None)

    if direct_group_id:
        return direct_group_id

    group_subject = getattr(obj, "group_subject", None)

    if group_subject is not None:
        return getattr(group_subject, "group_id", None)

    return None


def get_object_teacher_id(obj: Any) -> int | None:
    """
    Возвращает id преподавателя для объекта назначения.
    """

    return getattr(obj, "teacher_id", None)


def get_object_learner_id(obj: Any) -> int | None:
    """
    Возвращает id обучающегося для объекта зачисления.
    """

    return getattr(obj, "learner_id", None)


def get_payload_organization_ids_for_curriculum(
    data: Mapping[str, Any],
) -> set[int]:
    """
    Получает организации из payload учебного плана.
    """

    organization_id = _get_int_value(data, "organization_id")

    return {organization_id} if organization_id else set()


def get_payload_organization_ids_for_curriculum_item(
    data: Mapping[str, Any],
) -> set[int]:
    """
    Получает организации из payload элемента учебного плана.
    """

    curriculum_id = _get_int_value(data, "curriculum_id")

    if not curriculum_id:
        return set()

    return set(
        Curriculum.objects.filter(id=curriculum_id).values_list(
            "organization_id",
            flat=True,
        )
    )


def get_payload_organization_ids_for_group_subject(
    data: Mapping[str, Any],
) -> set[int]:
    """
    Получает организации из payload предмета группы.
    """

    organization_ids: set[int] = set()

    group_id = _get_int_value(data, "group_id")
    curriculum_item_id = _get_int_value(data, "curriculum_item_id")

    if group_id:
        organization_ids.update(
            StudyGroup.objects.filter(id=group_id).values_list(
                "organization_id",
                flat=True,
            )
        )

    if curriculum_item_id:
        organization_ids.update(
            CurriculumItem.objects.filter(id=curriculum_item_id).values_list(
                "curriculum__organization_id",
                flat=True,
            )
        )

    return organization_ids


def get_payload_organization_ids_for_teacher_group_subject(
    data: Mapping[str, Any],
) -> set[int]:
    """
    Получает организации из payload назначения преподавателя.
    """

    group_subject_id = _get_int_value(data, "group_subject_id")

    if not group_subject_id:
        return set()

    return set(
        GroupSubject.objects.filter(id=group_subject_id).values_list(
            "group__organization_id",
            flat=True,
        )
    )


def get_payload_organization_ids_for_learner_group_enrollment(
    data: Mapping[str, Any],
) -> set[int]:
    """
    Получает организации из payload академического зачисления.
    """

    group_id = _get_int_value(data, "group_id")

    if not group_id:
        return set()

    return set(
        StudyGroup.objects.filter(id=group_id).values_list(
            "organization_id",
            flat=True,
        )
    )


def user_can_manage_payload_organizations(
    *,
    user: User,
    organization_ids: set[int],
) -> bool:
    """
    Проверяет, что пользователь может менять данные указанных организаций.
    """

    if user_is_global_admin(user):
        return True

    if not organization_ids:
        return False

    available_organization_ids = get_user_available_organization_ids(user)

    return organization_ids.issubset(available_organization_ids)


def _get_int_value(
    data: Mapping[str, Any],
    key: str,
) -> int | None:
    """
    Безопасно получает int из request.data.
    """

    value = data.get(key)

    if value in (None, ""):
        return None

    if isinstance(value, list):
        value = value[0] if value else None

    if value in (None, ""):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None
