from __future__ import annotations

from django.urls import include, path

from .router import teacher_router

app_name = "course_teacher"

urlpatterns = [
    path("", include(teacher_router.urls)),
]
