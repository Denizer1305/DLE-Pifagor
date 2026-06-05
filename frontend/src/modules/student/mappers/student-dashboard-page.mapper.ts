import {
    createEmptyStudentStats,
    studentDashboardHero,
    studentDashboardSections,
    studentScheduleSection,
} from "@/modules/student/data/student-dashboard-content.data";
import { studentCreateModalContent } from "@/modules/student/data/student-dashboard.data";
import {
    createStudentCalendarContent,
    createStudentDayCard,
    createStudentMiniPlan,
} from "@/modules/student/mappers/student-dashboard-calendar.mapper";
import {
    createStudentProfile,
    createStudentShell,
} from "@/modules/student/mappers/student-dashboard-shell.mapper";
import type {
    StudentDashboardModel,
    StudentDashboardSummary,
} from "@/modules/student/types/student-dashboard.types";

export function createStudentDashboardModel(
    fullName = "",
    summary?: StudentDashboardSummary,
): StudentDashboardModel {
    const profile = createStudentProfile(fullName, summary);
    const dayCard = createStudentDayCard(summary);
    const miniPlan = createStudentMiniPlan(summary);

    return {
        shell: createStudentShell(profile),
        hero: studentDashboardHero,
        dayCard,
        miniPlan,
        heroSection: {
            hero: studentDashboardHero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайшее расписание",
            miniPlanIcon: "fas fa-clock",
        },
        calendarContent: createStudentCalendarContent(summary),
        calendarDays: summary?.calendar.days ?? [],
        createModal: studentCreateModalContent,
        notifications: {
            title: "Уведомления",
            createLabel: "Создать уведомление",
            items: summary?.notifications ?? [],
            emptyText: "Уведомлений пока нет.",
            actionLabel: "Посмотреть все уведомления",
            actionTo: { name: "student-notifications" },
        },
        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            removeLabel: "Удалить заметку",
            items: summary?.notes ?? [],
            emptyText: "Заметок пока нет.",
            actionLabel: "Открыть все заметки",
            actionTo: { name: "student-notes" },
        },
        profilePanel: {
            user: profile,
            title: "Профиль студента",
            subtitle: "Учебный профиль и настройки кабинета",
            actions: [
                { label: "Мой профиль", icon: "fas fa-user", to: { name: "student-profile" } },
                { label: "Настройки", icon: "fas fa-gear", to: { name: "student-settings" } },
                { label: "Выйти", icon: "fas fa-arrow-right-from-bracket", action: "logout" },
            ],
        },
        stats: summary?.stats ?? createEmptyStudentStats(),
        scheduleSection: studentScheduleSection,
        schedule: summary?.schedule ?? [],
        assignmentsSection: studentDashboardSections.assignments,
        assignments: summary?.assignments ?? [],
        coursesSection: studentDashboardSections.courses,
        courses: summary?.courses ?? [],
        activitySection: studentDashboardSections.activity,
        activityItems: summary?.activityItems ?? [],
        gradesSection: studentDashboardSections.grades,
        gradeRows: summary?.gradeRows ?? [],
        goalsSection: studentDashboardSections.goals,
        goals: summary?.goals ?? [],
    };
}
