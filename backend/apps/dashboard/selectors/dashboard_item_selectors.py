from __future__ import annotations

from apps.dashboard.models import DashboardItem


def get_dashboard_items_for_user(*, user):
    return DashboardItem.objects.filter(user=user).order_by("-item_date", "-created_at")


def get_dashboard_item_for_user(*, user, item_id):
    return DashboardItem.objects.filter(user=user, id=item_id).first()


def get_calendar_items_for_date(*, user, target_date):
    return DashboardItem.objects.filter(
        user=user,
        kind=DashboardItem.KindChoices.CALENDAR,
        item_date=target_date,
        notification_enabled=True,
    )


def get_note_items_in_period(*, user, starts_at, ends_at):
    return DashboardItem.objects.filter(
        user=user,
        kind=DashboardItem.KindChoices.NOTE,
        item_date__gte=starts_at.date(),
        item_date__lte=ends_at.date(),
        notification_enabled=True,
    )
