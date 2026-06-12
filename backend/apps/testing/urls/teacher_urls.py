from __future__ import annotations

from apps.testing.views.answer import TestAttemptAnswerViewSet
from apps.testing.views.attempt import TestAttemptViewSet
from apps.testing.views.bank import QuestionBankItemViewSet, QuestionBankOptionViewSet
from apps.testing.views.integrity import TestAttemptIntegrityReportViewSet
from apps.testing.views.option import TestQuestionOptionViewSet
from apps.testing.views.question import TestQuestionViewSet
from apps.testing.views.result import TestLearnerResultViewSet
from apps.testing.views.review import TestReviewViewSet
from apps.testing.views.test import TestViewSet
from rest_framework.routers import DefaultRouter

app_name = "testing_teacher"

router = DefaultRouter()

router.register(
    "tests",
    TestViewSet,
    basename="testing-teacher-tests",
)
router.register(
    "questions",
    TestQuestionViewSet,
    basename="testing-teacher-questions",
)
router.register(
    "options",
    TestQuestionOptionViewSet,
    basename="testing-teacher-options",
)
router.register(
    "attempts",
    TestAttemptViewSet,
    basename="testing-teacher-attempts",
)
router.register(
    "answers",
    TestAttemptAnswerViewSet,
    basename="testing-teacher-answers",
)
router.register(
    "results",
    TestLearnerResultViewSet,
    basename="testing-teacher-results",
)
router.register(
    "bank-items",
    QuestionBankItemViewSet,
    basename="testing-teacher-bank-items",
)
router.register(
    "bank-options",
    QuestionBankOptionViewSet,
    basename="testing-teacher-bank-options",
)
router.register(
    "integrity-reports",
    TestAttemptIntegrityReportViewSet,
    basename="testing-teacher-integrity-reports",
)
router.register(
    "review",
    TestReviewViewSet,
    basename="testing-teacher-review",
)

urlpatterns = router.urls
