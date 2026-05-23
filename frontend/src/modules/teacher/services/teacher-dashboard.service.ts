import { fetchTeacherDashboardSummary } from "@/modules/teacher/api/teacher-dashboard.api";
import {
    mapTeacherDashboardSummary,
    mapTeacherSummaryToPageModel,
} from "@/modules/teacher/mappers/teacher-dashboard.mapper";
import {
    createTeacherCalendarContent,
    teacherCreateModalContent,
    createTeacherNotificationsContent,
    createTeacherNotesContent,
    createTeacherProfilePanelContent,
    createTeacherShellConfig,
} from "@/modules/teacher/data/teacher-dashboard.data";
import type {
    TeacherDashboardPageModel,
    TeacherDashboardSummary,
    TeacherDashboardViewModel,
} from "@/modules/teacher/types/teacher-dashboard.types";

export interface TeacherDashboardServiceResult {
    summary: TeacherDashboardSummary;
    pageModel: TeacherDashboardPageModel;
    viewModel: TeacherDashboardViewModel;
}

export async function getTeacherDashboard(): Promise<TeacherDashboardServiceResult> {
    const dto = await fetchTeacherDashboardSummary();
    const summary = mapTeacherDashboardSummary(dto);

    return {
        summary,
        pageModel: mapTeacherSummaryToPageModel(summary),
        viewModel: {
            shell: createTeacherShellConfig(summary.profile, summary),
            calendarContent: createTeacherCalendarContent(summary.calendar.monthLabel),
            calendarDays: summary.calendar.days,
            notifications: createTeacherNotificationsContent(summary),
            notes: createTeacherNotesContent(summary),
            profilePanel: createTeacherProfilePanelContent(summary.profile),
            createModal: teacherCreateModalContent,
        },
    };
}
