import { fetchStudentDashboardSummary } from "@/modules/student/api/student-dashboard.api";
import { createStudentDashboardModel } from "@/modules/student/mappers/student-dashboard-page.mapper";
import { mapStudentDashboardSummary } from "@/modules/student/mappers/student-dashboard.mapper";
import type {
    StudentDashboardModel,
    StudentDashboardSummary,
} from "@/modules/student/types/student-dashboard.types";

export interface StudentDashboardServiceResult {
    summary: StudentDashboardSummary;
    model: StudentDashboardModel;
}

export async function getStudentDashboard(
    fallbackName = "",
): Promise<StudentDashboardServiceResult> {
    const dto = await fetchStudentDashboardSummary();
    const summary = mapStudentDashboardSummary(dto);

    return {
        summary,
        model: createStudentDashboardModel(fallbackName, summary),
    };
}
