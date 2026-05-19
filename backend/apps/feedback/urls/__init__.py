from django.urls import path

from apps.feedback.views import ContactFeedbackCreateAPIView

app_name = "feedback"

urlpatterns = [
    path(
        "contact/",
        ContactFeedbackCreateAPIView.as_view(),
        name="contact-feedback-create",
    ),
]