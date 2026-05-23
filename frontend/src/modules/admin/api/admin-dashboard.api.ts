import { httpClient } from "@/services/api/http.client";
import type { AdminDashboardSummaryDto } from "@/modules/admin/types/admin-dashboard.types";

const ADMIN_DASHBOARD_SUMMARY_URL = "/dashboard/admin/summary/";

export async function fetchAdminDashboardSummary(): Promise<AdminDashboardSummaryDto> {
    const response = await httpClient.get<AdminDashboardSummaryDto>(
        ADMIN_DASHBOARD_SUMMARY_URL,
    );

    return response.data;
}