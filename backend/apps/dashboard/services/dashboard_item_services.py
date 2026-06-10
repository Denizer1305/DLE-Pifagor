from __future__ import annotations

from apps.dashboard.models import DashboardItem
from apps.notifications.constants import NotificationSourceType
from apps.notifications.models import Notification
from apps.notifications.services.calendar_notification_services import (
    create_calendar_event_notification,
)
from apps.notifications.services.note_notification_services import (
    create_note_reminder_notification,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def create_dashboard_item(*, user, validated_data: dict) -> DashboardItem:
    item = DashboardItem.objects.create(user=user, **validated_data)

    create_notification_for_current_item(item=item)

    return item


def create_notification_for_current_item(*, item: DashboardItem) -> None:
    if not item.notification_enabled or item.item_date != timezone.localdate():
        return

    if item.kind == DashboardItem.KindChoices.CALENDAR:
        create_calendar_event_notification(
            user=item.user,
            event=item,
            target_date=item.item_date,
        )
        return

    create_note_reminder_notification(
        user=item.user,
        note=item,
        target_date=item.item_date,
    )


@transaction.atomic
def delete_dashboard_item(*, item: DashboardItem) -> None:
    source_type = (
        NotificationSourceType.CALENDAR_EVENT
        if item.kind == DashboardItem.KindChoices.CALENDAR
        else NotificationSourceType.NOTE
    )

    Notification.objects.filter(
        recipient=item.user,
        source_type=source_type,
        source_id=str(item.id),
    ).delete()
    item.delete()
