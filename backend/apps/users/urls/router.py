from __future__ import annotations

from apps.users.views import (
    GuardianLearnerViewSet,
    GuardianProfileViewSet,
    InviteCodeViewSet,
    LearnerProfileViewSet,
    ProfileViewSet,
    RoleViewSet,
    TeacherProfileViewSet,
    UserJoinRequestViewSet,
    UserRoleViewSet,
    UserSettingsViewSet,
    UserViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r"users",
    UserViewSet,
    basename="users",
)

router.register(
    r"profiles",
    ProfileViewSet,
    basename="profiles",
)

router.register(
    r"learner-profiles",
    LearnerProfileViewSet,
    basename="learner-profiles",
)

router.register(
    r"guardian-profiles",
    GuardianProfileViewSet,
    basename="guardian-profiles",
)

router.register(
    r"guardian-learner-links",
    GuardianLearnerViewSet,
    basename="guardian-learner-links",
)

router.register(
    r"teacher-profiles",
    TeacherProfileViewSet,
    basename="teacher-profiles",
)

router.register(
    r"roles",
    RoleViewSet,
    basename="roles",
)

router.register(
    r"user-roles",
    UserRoleViewSet,
    basename="user-roles",
)

router.register(
    r"invite-codes",
    InviteCodeViewSet,
    basename="invite-codes",
)

router.register(
    r"join-requests",
    UserJoinRequestViewSet,
    basename="join-requests",
)

router.register(
    r"settings",
    UserSettingsViewSet,
    basename="settings",
)


urlpatterns = router.urls
