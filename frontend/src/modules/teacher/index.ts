export { fetchTeacherDashboardSummary } from "@/modules/teacher/api/teacher-dashboard.api";
export { useTeacherDashboard } from "@/modules/teacher/composables/useTeacherDashboard";
export { useTeacherDashboardPresentation } from "@/modules/teacher/composables/useTeacherDashboardPresentation";
export { createTeacherNavigation } from "@/modules/teacher/data/teacher-navigation.data";

export {
    createTeacherCalendarContent,
    createTeacherDayCard,
    createTeacherNotificationsContent,
    createTeacherNotesContent,
    createTeacherProfilePanelContent,
    createTeacherShellConfig,
    teacherAiCardContent,
    teacherDashboardHero,
    teacherFallbackAvatar,
} from "@/modules/teacher/data/teacher-dashboard.data";

export {
    mapTeacherDashboardSummary,
    mapTeacherSummaryToPageModel,
} from "@/modules/teacher/mappers/teacher-dashboard.mapper";

export { getTeacherDashboard } from "@/modules/teacher/services/teacher-dashboard.service";

export type {
    TeacherCourseStatus,
    TeacherDashboardActivityItem,
    TeacherDashboardAttentionItem,
    TeacherDashboardCourse,
    TeacherDashboardCourseCardModel,
    TeacherDashboardHeroModel,
    TeacherDashboardJournalRow,
    TeacherDashboardPageModel,
    TeacherDashboardProfile,
    TeacherDashboardScheduleItem,
    TeacherDashboardStat,
    TeacherDashboardSummary,
    TeacherDashboardSummaryDto,
    TeacherDashboardTone,
    TeacherDashboardViewModel,
} from "@/modules/teacher/types/teacher-dashboard.types";
