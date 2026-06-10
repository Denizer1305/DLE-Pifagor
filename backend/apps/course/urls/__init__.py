from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("admin/", include("apps.course.urls.admin_urls")),
    path("teacher/", include("apps.course.urls.teacher_urls")),
    path("learner/", include("apps.course.urls.learner_urls")),
    path("public/", include("apps.course.urls.public_urls")),
]
