import { httpClient } from "@/services/api/http.client";
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

const NOTIFICATIONS_BASE_URL = "/notifications/";

export async function fetchNotifications(
    params: NotificationQueryParams = {},
): Promise<NotificationFeedDto> {
    const response = await httpClient.get<NotificationFeedDto>(
        `${NOTIFICATIONS_BASE_URL}me/`,
        {
            params,
        },
    );

    return response.data;
}

export async function fetchNotificationDetail(
    notificationId: number,
): Promise<NotificationDetailDto> {
    const response = await httpClient.get<NotificationDetailDto>(
        `${NOTIFICATIONS_BASE_URL}${notificationId}/`,
    );

    return response.data;
}

export async function fetchUnreadNotificationCount(): Promise<NotificationUnreadCountDto> {
    const response = await httpClient.get<NotificationUnreadCountDto>(
        `${NOTIFICATIONS_BASE_URL}me/unread-count/`,
    );

    return response.data;
}

export async function bootstrapNotifications(
    payload: NotificationBootstrapPayload = {
        reason: "dashboard_login",
    },
): Promise<NotificationBootstrapResponseDto> {
    const response = await httpClient.post<NotificationBootstrapResponseDto>(
        `${NOTIFICATIONS_BASE_URL}bootstrap/`,
        payload,
    );

    return response.data;
}

export async function markNotificationRead(
    notificationId: number,
): Promise<NotificationActionResponseDto> {
    const response = await httpClient.post<NotificationActionResponseDto>(
        `${NOTIFICATIONS_BASE_URL}${notificationId}/read/`,
        {},
    );

    return response.data;
}

export async function markAllNotificationsRead(): Promise<NotificationBulkActionResponseDto> {
    const response = await httpClient.post<NotificationBulkActionResponseDto>(
        `${NOTIFICATIONS_BASE_URL}read-all/`,
        {},
    );

    return response.data;
}

export async function completeNotification(
    notificationId: number,
): Promise<NotificationActionResponseDto> {
    const response = await httpClient.post<NotificationActionResponseDto>(
        `${NOTIFICATIONS_BASE_URL}${notificationId}/complete/`,
        {},
    );

    return response.data;
}

export async function deleteNotification(
    notificationId: number,
): Promise<NotificationDeleteResponseDto> {
    const response = await httpClient.delete<NotificationDeleteResponseDto>(
        `${NOTIFICATIONS_BASE_URL}${notificationId}/`,
    );

    return response.data;
}
