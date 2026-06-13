from __future__ import annotations

from apps.course.tests.factories import (
    create_course,
    create_course_enrollment,
    create_course_lesson,
    create_learner,
    create_study_group,
    create_superadmin,
    create_teacher,
)
from apps.testing.tests.factories.attempts import create_answer, create_attempt
from apps.testing.tests.factories.common import (
    extract_results,
    get_choice_value,
    unique_code,
    unique_email,
    unique_title,
)
from apps.testing.tests.factories.results import create_result, create_visible_result
from apps.testing.tests.factories.structure import (
    create_choice_question_with_options,
    create_option,
    create_question,
    create_test,
)
from apps.testing.tests.factories.bank import (
    create_bank_item,
    create_bank_item_with_options,
    create_bank_option,
    create_published_bank_item,
)
from apps.testing.tests.factories.integrity import (
    create_integrity_report,
    create_risky_integrity_report,
)

__all__ = [
    "create_answer",
    "create_attempt",
    "create_choice_question_with_options",
    "create_course",
    "create_course_enrollment",
    "create_course_lesson",
    "create_learner",
    "create_option",
    "create_question",
    "create_result",
    "create_study_group",
    "create_superadmin",
    "create_teacher",
    "create_test",
    "create_visible_result",
    "extract_results",
    "get_choice_value",
    "unique_code",
    "unique_email",
    "unique_title",
    "create_bank_item",
    "create_bank_item_with_options",
    "create_bank_option",
    "create_integrity_report",
    "create_published_bank_item",
    "create_risky_integrity_report",
]
