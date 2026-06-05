import {
    deleteDashboardItem,
    fetchDashboardItems,
    postDashboardItem,
} from "@/components/dashboard/api/dashboard-items.api";
import type {
    DashboardItemCreatePayload,
    DashboardItemDto,
} from "@/components/dashboard/types/dashboard-items.types";

export function getDashboardItems(): Promise<DashboardItemDto[]> {
    return fetchDashboardItems();
}

export function createDashboardItem(
    payload: DashboardItemCreatePayload,
): Promise<DashboardItemDto> {
    return postDashboardItem(payload);
}

export function removeDashboardItem(itemId: number): Promise<void> {
    return deleteDashboardItem(itemId);
}
