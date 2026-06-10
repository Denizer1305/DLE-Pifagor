import { httpClient } from "@/services/api/http.client";
import type {
    DashboardItemCreatePayload,
    DashboardItemDto,
} from "@/components/dashboard/types/dashboard-items.types";

const DASHBOARD_ITEMS_URL = "/dashboard/me/items/";

export async function fetchDashboardItems(): Promise<DashboardItemDto[]> {
    const response = await httpClient.get<DashboardItemDto[]>(DASHBOARD_ITEMS_URL);

    return response.data;
}

export async function postDashboardItem(
    payload: DashboardItemCreatePayload,
): Promise<DashboardItemDto> {
    const response = await httpClient.post<DashboardItemDto>(DASHBOARD_ITEMS_URL, {
        kind: payload.kind,
        title: payload.title,
        text: payload.text,
        date: payload.date,
        event_type: payload.eventType,
        notification_enabled: payload.notificationEnabled,
    });

    return response.data;
}

export async function deleteDashboardItem(itemId: number): Promise<void> {
    await httpClient.delete(`${DASHBOARD_ITEMS_URL}${itemId}/`);
}
