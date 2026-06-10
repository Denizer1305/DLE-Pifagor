from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("admin/", include("apps.materials.urls.admin_urls")),
    path("teacher/", include("apps.materials.urls.teacher_urls")),
    path("learner/", include("apps.materials.urls.learner_urls")),
    path("public/", include("apps.materials.urls.public_urls")),
]
