import { httpClient } from "@/services/api/http.client";
import type { TeacherDashboardSummaryDto } from "@/modules/teacher/types/teacher-dashboard.types";

const TEACHER_DASHBOARD_SUMMARY_URL = "/dashboard/teacher/summary/";

export async function fetchTeacherDashboardSummary(): Promise<TeacherDashboardSummaryDto> {
    const response = await httpClient.get<TeacherDashboardSummaryDto>(
        TEACHER_DASHBOARD_SUMMARY_URL,
    );

    return response.data;
}
