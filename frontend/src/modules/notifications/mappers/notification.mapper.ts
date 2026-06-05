import {
    notificationCategoryLabels,
    notificationLevelIcons,
    notificationLevelLabels,
    notificationStatusLabels,
} from "@/modules/notifications/data/notification-options.data";
import type {
    NotificationDto,
    NotificationFeedDto,
    NotificationFeedViewModel,
    NotificationViewModel,
} from "@/modules/notifications/types/notifications.types";

export function mapNotificationDtoToViewModel(
    dto: NotificationDto,
): NotificationViewModel {
    return {
        id: dto.id,
        title: dto.title,
        message: dto.message,
        type: dto.notification_type,
        category: dto.category,
        categoryLabel: notificationCategoryLabels[dto.category] || dto.category,
        level: dto.level,
        levelLabel: notificationLevelLabels[dto.level] || dto.level,
        levelIcon: notificationLevelIcons[dto.level] || "fas fa-bell",
        status: dto.status,
        statusLabel: notificationStatusLabels[dto.status] || dto.status,
        isUnread: dto.is_unread || dto.status === "unread",
        hasAction: dto.has_action,
        actionLabel: dto.action_label,
        actionUrl: dto.action_url,
        createdAt: dto.created_at,
        createdAtLabel: formatNotificationDate(dto.created_at),
        eventAt: dto.event_at,
        eventAtLabel: dto.event_at ? formatNotificationDate(dto.event_at) : "",
    };
}

export function mapNotificationFeedDtoToViewModel(
    dto: NotificationFeedDto,
): NotificationFeedViewModel {
    return {
        unreadCount: dto.unread_count,
        items: dto.items.map(mapNotificationDtoToViewModel),
    };
}

export function formatNotificationDate(value: string): string {
    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    }).format(date);
}

export function isNotificationImportant(notification: NotificationViewModel): boolean {
    return notification.level === "warning" || notification.level === "danger";
}

export function getNotificationActionTarget(actionUrl: string): string {
    if (!actionUrl) {
        return "";
    }

    if (actionUrl.startsWith("/")) {
        return actionUrl;
    }

    return `/${actionUrl}`;
}