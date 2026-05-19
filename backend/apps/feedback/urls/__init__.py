from apps.feedback.views import ContactFeedbackCreateAPIView
from django.urls import path

app_name = "feedback"

urlpatterns = [
    path(
        "contact/",
        ContactFeedbackCreateAPIView.as_view(),
        name="contact-feedback-create",
    ),
]
