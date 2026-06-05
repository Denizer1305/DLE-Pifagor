export { fetchParentDashboardSummary } from "@/modules/parent/api/parent-dashboard.api";
export { useParentDashboard } from "@/modules/parent/composables/useParentDashboard";
export { useParentDashboardPresentation } from "@/modules/parent/composables/useParentDashboardPresentation";

export {
    parentCreateModalContent,
    parentDashboardPageUi,
} from "@/modules/parent/data/parent-dashboard.data";

export { createParentDashboardModel } from "@/modules/parent/mappers/parent-dashboard-page.mapper";
export { mapParentDashboardSummary } from "@/modules/parent/mappers/parent-dashboard.mapper";
export { getParentDashboard } from "@/modules/parent/services/parent-dashboard.service";

export type {
    ParentCalendarContent,
    ParentDashboardModel,
    ParentDashboardSectionContent,
    ParentDashboardSummary,
    ParentDashboardProfile,
    ParentGradeRow,
} from "@/modules/parent/types/parent-dashboard.types";
export type { ParentDashboardSummaryDto } from "@/modules/parent/types/parent-dashboard-dto.types";
