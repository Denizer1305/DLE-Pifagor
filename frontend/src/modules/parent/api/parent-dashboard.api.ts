import { httpClient } from "@/services/api/http.client";
import type { ParentDashboardSummaryDto } from "@/modules/parent/types/parent-dashboard-dto.types";

const PARENT_DASHBOARD_SUMMARY_URL = "/dashboard/parent/summary/";

export async function fetchParentDashboardSummary(): Promise<ParentDashboardSummaryDto> {
    const response = await httpClient.get<ParentDashboardSummaryDto>(
        PARENT_DASHBOARD_SUMMARY_URL,
    );

    return response.data;
}
