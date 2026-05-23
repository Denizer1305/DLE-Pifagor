import { fetchAdminDashboardSummary } from "@/modules/admin/api/admin-dashboard.api";
import { mapAdminDashboardSummary } from "@/modules/admin/mappers/admin-dashboard.mapper";
import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";

export async function getAdminDashboardSummary(): Promise<AdminDashboardSummary> {
    const response = await fetchAdminDashboardSummary();

    return mapAdminDashboardSummary(response);
}
