from __future__ import annotations

from apps.users.views import (
    ForgotPasswordView,
    GuardianRegistrationView,
    LearnerRegistrationView,
    LoginView,
    LogoutView,
    MinorLearnerRegistrationView,
    RefreshTokenView,
    ResetPasswordView,
    TeacherRegistrationView,
    VerifyEmailView,
)
from django.urls import path

app_name = "auth"


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        RefreshTokenView.as_view(),
        name="refresh",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "verify-email/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "password/forgot/",
        ForgotPasswordView.as_view(),
        name="password-forgot",
    ),
    path(
        "password/reset/",
        ResetPasswordView.as_view(),
        name="password-reset",
    ),
    path(
        "register/teacher/",
        TeacherRegistrationView.as_view(),
        name="register-teacher",
    ),
    path(
        "register/learner/",
        LearnerRegistrationView.as_view(),
        name="register-learner",
    ),
    path(
        "register/guardian/",
        GuardianRegistrationView.as_view(),
        name="register-guardian",
    ),
    path(
        "register/minor-learner/",
        MinorLearnerRegistrationView.as_view(),
        name="register-minor-learner",
    ),
]
