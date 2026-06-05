from apps.feedback.views import (
    ContactFeedbackCreateAPIView,
    FeedbackAdminListAPIView,
    FeedbackAdminStatusAPIView,
)
from django.urls import path

app_name = "feedback"

urlpatterns = [
    path(
        "contact/",
        ContactFeedbackCreateAPIView.as_view(),
        name="contact-feedback-create",
    ),
    path(
        "admin/requests/",
        FeedbackAdminListAPIView.as_view(),
        name="feedback-admin-list",
    ),
    path(
        "admin/requests/<int:request_id>/",
        FeedbackAdminStatusAPIView.as_view(),
        name="feedback-admin-status",
    ),
]
