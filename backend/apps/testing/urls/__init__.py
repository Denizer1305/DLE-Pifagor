from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("admin/", include("apps.testing.urls.admin_urls")),
    path("teacher/", include("apps.testing.urls.teacher_urls")),
    path("learner/", include("apps.testing.urls.learner_urls")),
]
