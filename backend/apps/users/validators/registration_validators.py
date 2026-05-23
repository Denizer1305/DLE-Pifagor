from __future__ import annotations

from datetime import date

from apps.users.constants.roles import RoleCode
from apps.users.validators.user_validators import (
    validate_unique_email,
    validate_unique_phone,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MIN_SELF_REGISTRATION_AGE = 14


def calculate_age(birth_date: date) -> int:
    """
    Вычисляет возраст пользователя по дате рождения.

    Args:
        birth_date:
            Дата рождения.

    Returns:
        int: Возраст пользователя в полных годах.
    """

    today = date.today()

    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def validate_registration_role(role_code: str) -> None:
    """
    Проверяет роль, выбранную при регистрации.

    Args:
        role_code:
            Код роли.

    Raises:
        ValidationError: Если роль недопустима для самостоятельной регистрации.
    """

    allowed_roles = {
        RoleCode.LEARNER,
        RoleCode.GUARDIAN,
        RoleCode.TEACHER,
    }

    if role_code not in allowed_roles:
        raise ValidationError(_("Недопустимая роль для самостоятельной регистрации."))


def validate_registration_contacts(
    *,
    email: str,
    phone: str,
) -> None:
    """
    Проверяет контактные данные при регистрации.

    Args:
        email:
            Email пользователя.
        phone:
            Телефон пользователя.

    Raises:
        ValidationError: Если email или телефон уже используются.
    """

    validate_unique_email(email)
    validate_unique_phone(phone)


def validate_learner_self_registration_age(birth_date: date | None) -> None:
    """
    Проверяет возраст учащегося для самостоятельной регистрации.

    Учащийся может самостоятельно регистрироваться, если ему 14 лет или больше.
    Если ребёнку меньше 14 лет, регистрацию должен выполнять родитель.

    Args:
        birth_date:
            Дата рождения учащегося.

    Raises:
        ValidationError: Если дата рождения не указана или учащемуся меньше 14 лет.
    """

    if birth_date is None:
        raise ValidationError(_("Для регистрации учащегося требуется дата рождения."))

    age = calculate_age(birth_date)

    if age < MIN_SELF_REGISTRATION_AGE:
        raise ValidationError(
            _(
                "Учащиеся младше 14 лет регистрируются через родителя или законного представителя."
            )
        )


def validate_minor_learner_age(birth_date: date | None) -> None:
    """
    Проверяет, что ребёнок действительно младше 14 лет.

    Args:
        birth_date:
            Дата рождения ребёнка.

    Raises:
        ValidationError: Если дата рождения не указана или ребёнку уже 14 лет.
    """

    if birth_date is None:
        raise ValidationError(_("Для регистрации ребёнка требуется дата рождения."))

    age = calculate_age(birth_date)

    if age >= MIN_SELF_REGISTRATION_AGE:
        raise ValidationError(
            _("Этот сценарий регистрации доступен только для детей младше 14 лет.")
        )


def validate_guardian_can_create_minor_learner(guardian) -> None:
    """
    Проверяет, может ли родитель создать аккаунт ребёнка младше 14 лет.

    Args:
        guardian:
            Пользователь родителя.

    Raises:
        ValidationError: Если пользователь неактивен или не подтверждён.
    """

    if not guardian:
        raise ValidationError(_("Родитель не указан."))

    if not guardian.is_active:
        raise ValidationError(_("Аккаунт родителя неактивен."))

    if not guardian.is_email_verified:
        raise ValidationError(_("Email родителя должен быть подтверждён."))
