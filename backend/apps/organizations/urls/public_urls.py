from __future__ import annotations

from apps.organizations.views import (
    CurrentUserOrganizationAPIView,
    DefaultPublicOrganizationAPIView,
    PublicOrganizationListAPIView,
    PublicTeachersPageAPIView,
)
from django.urls import path

app_name = "organizations"

urlpatterns = [
    path(
        "public/",
        PublicOrganizationListAPIView.as_view(),
        name="public-list",
    ),
    path(
        "public/default/",
        DefaultPublicOrganizationAPIView.as_view(),
        name="public-default",
    ),
    path(
        "current/",
        CurrentUserOrganizationAPIView.as_view(),
        name="current",
    ),
    path(
        "public/teachers/",
        PublicTeachersPageAPIView.as_view(),
        name="public-teachers-page",
    ),
]
