from __future__ import annotations

from django.urls import include, path

from .router import learner_router

app_name = "course_learner"

urlpatterns = [
    path("", include(learner_router.urls)),
]
