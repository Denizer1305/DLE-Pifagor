import { httpClient } from "@/services/api/http.client";
import type { StudentDashboardSummaryDto } from "@/modules/student/types/student-dashboard.types";

const STUDENT_DASHBOARD_SUMMARY_URL = "/dashboard/student/summary/";

export async function fetchStudentDashboardSummary(): Promise<StudentDashboardSummaryDto> {
    const response = await httpClient.get<StudentDashboardSummaryDto>(
        STUDENT_DASHBOARD_SUMMARY_URL,
    );

    return response.data;
}
