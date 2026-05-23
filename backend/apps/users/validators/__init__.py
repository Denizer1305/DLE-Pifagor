"""
Валидаторы приложения users.

Валидаторы выполняют точечные проверки данных:
    - уникальность email и телефона;
    - допустимость роли регистрации;
    - возраст учащегося;
    - корректность контекста кода приглашения.

Важно:
    Валидаторы не должны выполнять сложные бизнес-сценарии.
    Сложные операции остаются в users/services/.
"""

from apps.users.validators.invite_code_validators import (
    validate_invite_code_context,
    validate_invite_code_purpose,
    validate_invite_code_required,
)
from apps.users.validators.registration_validators import (
    MIN_SELF_REGISTRATION_AGE,
    calculate_age,
    validate_guardian_can_create_minor_learner,
    validate_learner_self_registration_age,
    validate_minor_learner_age,
    validate_registration_contacts,
    validate_registration_role,
)
from apps.users.validators.user_validators import (
    validate_unique_email,
    validate_unique_phone,
    validate_user_can_login,
    validate_user_is_not_anonymized,
)

__all__ = [
    "MIN_SELF_REGISTRATION_AGE",
    "calculate_age",
    "validate_guardian_can_create_minor_learner",
    "validate_invite_code_context",
    "validate_invite_code_purpose",
    "validate_invite_code_required",
    "validate_learner_self_registration_age",
    "validate_minor_learner_age",
    "validate_registration_contacts",
    "validate_registration_role",
    "validate_unique_email",
    "validate_unique_phone",
    "validate_user_can_login",
    "validate_user_is_not_anonymized",
]
