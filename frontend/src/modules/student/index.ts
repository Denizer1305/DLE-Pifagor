export { fetchStudentDashboardSummary } from "@/modules/student/api/student-dashboard.api";
export { useStudentDashboard } from "@/modules/student/composables/useStudentDashboard";
export { useStudentDashboardPresentation } from "@/modules/student/composables/useStudentDashboardPresentation";

export {
    studentCreateModalContent,
    studentDashboardPageUi,
} from "@/modules/student/data/student-dashboard.data";

export { mapStudentDashboardSummary } from "@/modules/student/mappers/student-dashboard.mapper";
export { createStudentDashboardModel } from "@/modules/student/mappers/student-dashboard-page.mapper";
export { getStudentDashboard } from "@/modules/student/services/student-dashboard.service";

export type {
    StudentDashboardCalendar,
    StudentDashboardDayStats,
    StudentDashboardModel,
    StudentDashboardProfile,
    StudentDashboardSectionContent,
    StudentDashboardSummary,
    StudentDashboardSummaryDto,
    StudentGradeRow,
} from "@/modules/student/types/student-dashboard.types";
