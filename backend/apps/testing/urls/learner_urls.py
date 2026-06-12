from __future__ import annotations

from apps.testing.views.answer import TestAttemptAnswerViewSet
from apps.testing.views.attempt import TestAttemptViewSet
from apps.testing.views.result import TestLearnerResultViewSet
from apps.testing.views.taking import TestTakingViewSet
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
router.register(
    "taking",
    TestTakingViewSet,
    basename="testing-learner-taking",
)

urlpatterns = router.urls
