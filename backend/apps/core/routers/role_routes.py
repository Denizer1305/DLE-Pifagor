from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RoleRoute:
    """
    Описание маршрута для role-based router.

    Attributes:
        prefix: URL-префикс внутри router.
        viewset: ViewSet-класс.
        route_name: Короткое имя маршрута для basename.
    """

    prefix: str
    viewset: type[Any]
    route_name: str


RawRoleRoute = RoleRoute | tuple[str, type[Any], str]


def build_role_basename(
    *,
    app_label: str,
    role_prefix: str,
    route_name: str,
) -> str:
    """
    Собирает basename для role-based router.

    Example:
        app_label="assignments"
        role_prefix="teacher"
        route_name="submissions"

        Result:
        "assignments-teacher-submissions"
    """

    return "-".join(
        part.strip("-")
        for part in (
            app_label,
            role_prefix,
            route_name,
        )
        if part
    )


def normalize_role_route(route: RawRoleRoute) -> RoleRoute:
    """
    Приводит tuple-описание маршрута к RoleRoute.
    """

    if isinstance(route, RoleRoute):
        return route

    prefix, viewset, route_name = route

    return RoleRoute(
        prefix=prefix,
        viewset=viewset,
        route_name=route_name,
    )


def register_role_routes(
    *,
    router,
    routes: Iterable[RawRoleRoute],
    app_label: str,
    role_prefix: str,
):
    """
    Регистрирует набор маршрутов для конкретной роли.

    Helper не создаёт router сам, а только регистрирует routes
    в уже созданный DRF router.

    Example:
        router = DefaultRouter()

        register_role_routes(
            router=router,
            routes=ASSIGNMENT_TEACHER_ROUTES,
            app_label="assignments",
            role_prefix="teacher",
        )
    """

    for raw_route in routes:
        route = normalize_role_route(raw_route)
        basename = build_role_basename(
            app_label=app_label,
            role_prefix=role_prefix,
            route_name=route.route_name,
        )

        router.register(
            route.prefix,
            route.viewset,
            basename=basename,
        )

    return router
