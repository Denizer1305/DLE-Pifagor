from __future__ import annotations

from dataclasses import dataclass

from apps.dashboard.selectors.common import get_optional_model, model_has_field
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.onboarding import JoinRequestStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import UserJoinRequest, UserRole
from django.contrib.auth import get_user_model

User = get_user_model()


@dataclass(frozen=True)
class DashboardCount:
    key: str
    label: str
    value: int
    caption: str
    icon: str
    tone: str = "primary"


def count_users_by_role(role_code: str) -> int:
    """
    Считает уникальных пользователей с активной ролью.
    """

    return (
        UserRole.objects.filter(
            role__code=role_code,
            role__is_active=True,
            status=UserRoleStatus.ACTIVE,
        )
        .values("user_id")
        .distinct()
        .count()
    )


def count_feedback_new() -> int:
    """
    Считает новые обращения обратной связи.
    """

    FeedbackRequest = get_optional_model("feedback", "FeedbackRequest")

    if FeedbackRequest is None:
        return 0

    return FeedbackRequest.objects.filter(status="new").count()


def count_organizations() -> int:
    """
    Считает подключённые организации.
    """

    Organization = get_optional_model("organizations", "Organization")

    if Organization is None:
        return 0

    queryset = Organization.objects.all()

    if model_has_field(Organization, "is_active"):
        queryset = queryset.filter(is_active=True)

    return queryset.count()


def count_active_courses() -> int:
    """
    Считает активные курсы.

    Поддерживает несколько возможных имён моделей, чтобы dashboard не был
    жёстко связан с ещё нестабилизированным courses-модулем.
    """

    for model_name in ["Course", "CourseProgram"]:
        Course = get_optional_model("courses", model_name)

        if Course is None:
            continue

        queryset = Course.objects.all()

        if model_has_field(Course, "is_active"):
            queryset = queryset.filter(is_active=True)

        if model_has_field(Course, "status"):
            queryset = queryset.exclude(
                status__in=[
                    "archived",
                    "draft",
                ],
            )

        return queryset.count()

    return 0


def get_admin_stats_payload() -> list[dict]:
    """
    Формирует карточки статистики для главной страницы администратора.
    """

    stats = [
        DashboardCount(
            key="users",
            label="Пользователи",
            value=User.objects.count(),
            caption="Все аккаунты платформы",
            icon="fas fa-users",
            tone="primary",
        ),
        DashboardCount(
            key="teachers",
            label="Преподаватели",
            value=count_users_by_role(RoleCode.TEACHER),
            caption="Активные преподавательские роли",
            icon="fas fa-chalkboard-user",
            tone="success",
        ),
        DashboardCount(
            key="learners",
            label="Студенты",
            value=count_users_by_role(RoleCode.LEARNER),
            caption="Активные учащиеся",
            icon="fas fa-user-graduate",
            tone="violet",
        ),
        DashboardCount(
            key="guardians",
            label="Родители",
            value=count_users_by_role(RoleCode.GUARDIAN),
            caption="Активные родительские аккаунты",
            icon="fas fa-people-roof",
            tone="primary",
        ),
        DashboardCount(
            key="join_requests",
            label="Заявки",
            value=UserJoinRequest.objects.filter(
                status=JoinRequestStatus.PENDING,
            ).count(),
            caption="Ожидают рассмотрения",
            icon="fas fa-user-check",
            tone="warning",
        ),
        DashboardCount(
            key="feedback",
            label="Обращения",
            value=count_feedback_new(),
            caption="Новые обращения поддержки",
            icon="fas fa-envelope-open-text",
            tone="warning",
        ),
        DashboardCount(
            key="organizations",
            label="Организации",
            value=count_organizations(),
            caption="Подключённые образовательные организации",
            icon="fas fa-building-columns",
            tone="primary",
        ),
        DashboardCount(
            key="courses",
            label="Курсы",
            value=count_active_courses(),
            caption="Активные учебные курсы",
            icon="fas fa-book-open",
            tone="success",
        ),
    ]

    return [
        {
            "key": item.key,
            "label": item.label,
            "value": item.value,
            "caption": item.caption,
            "icon": item.icon,
            "tone": item.tone,
        }
        for item in stats
    ]
