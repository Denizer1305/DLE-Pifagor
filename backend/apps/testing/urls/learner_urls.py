from __future__ import annotations

from apps.testing.views.answer import TestAttemptAnswerViewSet
from apps.testing.views.attempt import TestAttemptViewSet
from apps.testing.views.option import TestQuestionOptionViewSet
from apps.testing.views.question import TestQuestionViewSet
from apps.testing.views.result import TestLearnerResultViewSet
from apps.testing.views.test import TestViewSet
from rest_framework.routers import DefaultRouter

app_name = "testing_learner"

router = DefaultRouter()
router.register(
    "tests",
    TestViewSet,
    basename="testing-learner-tests",
)
router.register(
    "questions",
    TestQuestionViewSet,
    basename="testing-learner-questions",
)
router.register(
    "options",
    TestQuestionOptionViewSet,
    basename="testing-learner-options",
)
router.register(
    "attempts",
    TestAttemptViewSet,
    basename="testing-learner-attempts",
)
router.register(
    "answers",
    TestAttemptAnswerViewSet,
    basename="testing-learner-answers",
)
router.register(
    "results",
    TestLearnerResultViewSet,
    basename="testing-learner-results",
)

urlpatterns = router.urls
