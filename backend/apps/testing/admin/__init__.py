from __future__ import annotations

from apps.testing.admin.answer import admin as answer_admin
from apps.testing.admin.attempt import admin as attempt_admin
from apps.testing.admin.bank import admin as bank_admin
from apps.testing.admin.integrity import admin as integrity_admin
from apps.testing.admin.question import admin as question_admin
from apps.testing.admin.result import admin as result_admin
from apps.testing.admin.test import admin as test_admin

__all__ = [
    "answer_admin",
    "attempt_admin",
    "bank_admin",
    "integrity_admin",
    "question_admin",
    "result_admin",
    "test_admin",
]
