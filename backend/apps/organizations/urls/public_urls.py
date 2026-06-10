from __future__ import annotations

from apps.organizations.views import (
    CurrentUserOrganizationAPIView,
    DefaultPublicOrganizationAPIView,
    PublicOrganizationListAPIView,
    PublicTeachersPageAPIView,
)
from django.urls import path

urlpatterns = [
    path(
        "public/",
        PublicOrganizationListAPIView.as_view(),
        name="public-organizations-list",
    ),
    path(
        "public/default/",
        DefaultPublicOrganizationAPIView.as_view(),
        name="public-organizations-default",
    ),
    path(
        "public/teachers/",
        PublicTeachersPageAPIView.as_view(),
        name="public-teachers-page",
    ),
    path(
        "current/",
        CurrentUserOrganizationAPIView.as_view(),
        name="current-organization",
    ),
]
