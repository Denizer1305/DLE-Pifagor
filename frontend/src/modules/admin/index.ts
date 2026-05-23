export { fetchAdminDashboardSummary } from "@/modules/admin/api/admin-dashboard.api";
export { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";

export {
    adminAiCardContent,
    adminDayCardContent,
    adminFallbackAvatar,
    adminIntroContent,
    createAdminCalendarContent,
    createAdminNotificationsContent,
    createAdminNotesContent,
    createAdminProfilePanelContent,
    createAdminShellConfig,
} from "@/modules/admin/data/admin-dashboard.data";

export { createAdminNavigation } from "@/modules/admin/data/admin-navigation.data";

export {
    mapAdminDashboardSummary,
    mapAdminStatsToDashboardCards,
    mapAuditEventsToTimeline,
    mapFeedbackRequestsToSection,
    mapJoinRequestsToSection,
    mapRecentUsersToSection,
    mapSystemHealthToSection,
} from "@/modules/admin/mappers/admin-dashboard.mapper";

export type {
    AdminDashboardAuditActor,
    AdminDashboardAuditEvent,
    AdminDashboardCalendar,
    AdminDashboardFeedbackRequest,
    AdminDashboardJoinRequest,
    AdminDashboardProfile,
    AdminDashboardQuickAction,
    AdminDashboardStat,
    AdminDashboardSummary,
    AdminDashboardSummaryDto,
    AdminDashboardSystemCheck,
    AdminDashboardSystemHealth,
    AdminDashboardTone,
    AdminDashboardUserShort,
    AdminDashboardViewModel,
    AdminSystemStatus,
} from "@/modules/admin/types/admin-dashboard.types";
