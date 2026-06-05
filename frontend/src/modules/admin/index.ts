export { fetchAdminDashboardSummary } from "@/modules/admin/api/admin-dashboard.api";
export {
    fetchAdminFeedbackRequests,
    patchAdminFeedbackStatus,
} from "@/modules/admin/api/admin-feedback.api";
export {
    fetchAdminUserDetail,
    fetchAdminUsers,
    patchAdminUser,
    postAdminUserStatusAction,
} from "@/modules/admin/api/admin-users.api";
export { useAdminDashboard } from "@/modules/admin/composables/useAdminDashboard";
export { useAdminDashboardPresentation } from "@/modules/admin/composables/useAdminDashboardPresentation";
export { useAdminFeedback } from "@/modules/admin/composables/useAdminFeedback";
export { useAdminUserDetail } from "@/modules/admin/composables/useAdminUserDetail";
export { useAdminUserEdit } from "@/modules/admin/composables/useAdminUserEdit";
export { useAdminUsers } from "@/modules/admin/composables/useAdminUsers";

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
    adminFeedbackContent,
    adminFeedbackStatusOptions,
    adminFeedbackTopicOptions,
} from "@/modules/admin/data/admin-feedback.data";

export {
    mapAdminDashboardSummary,
    mapAdminStatsToDashboardCards,
    mapAuditEventsToTimeline,
    mapFeedbackRequestsToSection,
    mapJoinRequestsToSection,
    mapRecentUsersToSection,
    mapSystemHealthToSection,
} from "@/modules/admin/mappers/admin-dashboard.mapper";
export {
    mapAdminFeedbackList,
    mapAdminFeedbackRequest,
} from "@/modules/admin/mappers/admin-feedback.mapper";
export {
    createAdminUserEditForm,
    mapAdminUserDetail,
    mapAdminUserEditPayload,
    mapAdminUsersList,
} from "@/modules/admin/mappers/admin-users.mapper";

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
export type {
    AdminFeedbackFilters,
    AdminFeedbackList,
    AdminFeedbackRequest,
    AdminFeedbackStatus,
    AdminFeedbackSummary,
    AdminFeedbackTopic,
} from "@/modules/admin/types/admin-feedback.types";
export type {
    AdminUserDetailDto,
    AdminUserDetailModel,
    AdminUserEditForm,
    AdminUserListDto,
    AdminUserRoleDto,
    AdminUserRoleGroup,
    AdminUsersFilters,
    AdminUsersListItem,
    AdminUsersListModel,
    AdminUserStatusAction,
    AdminUserUpdatePayload,
} from "@/modules/admin/types/admin-users.types";
