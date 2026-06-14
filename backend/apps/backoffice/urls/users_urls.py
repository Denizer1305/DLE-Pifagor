from __future__ import annotations

from apps.backoffice.views.users import BackofficeUserViewSet
from apps.core.routers import register_role_routes
from rest_framework.routers import DefaultRouter

app_name = "backoffice_users"

router = DefaultRouter()

BACKOFFICE_USER_ROUTES = (("", BackofficeUserViewSet, "users"),)

register_role_routes(
    router=router,
    routes=BACKOFFICE_USER_ROUTES,
    app_label="backoffice",
    role_prefix="",
)

urlpatterns = router.urls
