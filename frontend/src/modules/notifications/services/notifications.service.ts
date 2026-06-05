import {
    bootstrapNotifications,
    completeNotification,
    deleteNotification,
    fetchNotificationDetail,
    fetchNotifications,
    fetchUnreadNotificationCount,
    markAllNotificationsRead,
    markNotificationRead,
} from "@/modules/notifications/api/notifications.api";
import type {
    NotificationActionResponseDto,
    NotificationBootstrapPayload,
    NotificationBootstrapResponseDto,
    NotificationBulkActionResponseDto,
    NotificationDeleteResponseDto,
    NotificationDetailDto,
    NotificationFeedDto,
    NotificationQueryParams,
    NotificationUnreadCountDto,
} from "@/modules/notifications/types/notifications.types";

export function getNotifications(
    params: NotificationQueryParams = {},
): Promise<NotificationFeedDto> {
    return fetchNotifications(params);
}

export function getNotificationDetail(
    notificationId: number,
): Promise<NotificationDetailDto> {
    return fetchNotificationDetail(notificationId);
}

export function getUnreadNotificationCount(): Promise<NotificationUnreadCountDto> {
    return fetchUnreadNotificationCount();
}

export function runNotificationBootstrap(
    payload: NotificationBootstrapPayload = {
        reason: "dashboard_login",
    },
): Promise<NotificationBootstrapResponseDto> {
    return bootstrapNotifications(payload);
}

export function readNotification(
    notificationId: number,
): Promise<NotificationActionResponseDto> {
    return markNotificationRead(notificationId);
}

export function readAllNotifications(): Promise<NotificationBulkActionResponseDto> {
    return markAllNotificationsRead();
}

export function finishNotification(
    notificationId: number,
): Promise<NotificationActionResponseDto> {
    return completeNotification(notificationId);
}

export function removeNotification(
    notificationId: number,
): Promise<NotificationDeleteResponseDto> {
    return deleteNotification(notificationId);
}