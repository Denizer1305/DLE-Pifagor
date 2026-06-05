import { fetchParentDashboardSummary } from "@/modules/parent/api/parent-dashboard.api";
import { mapParentDashboardSummary } from "@/modules/parent/mappers/parent-dashboard.mapper";
import type { ParentDashboardSummary } from "@/modules/parent/types/parent-dashboard.types";

export async function getParentDashboard(): Promise<ParentDashboardSummary> {
    const dto = await fetchParentDashboardSummary();

    return mapParentDashboardSummary(dto);
}
