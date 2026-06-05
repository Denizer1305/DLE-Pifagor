import {
    createEmptyParentStats,
    parentDashboardHero,
    parentDashboardSections,
} from "@/modules/parent/data/parent-dashboard-content.data";
import { parentCreateModalContent } from "@/modules/parent/data/parent-dashboard.data";
import {
    createEmptyParentCalendarDays,
    createParentCalendarContent,
    createParentDayCard,
    createParentMiniPlan,
} from "@/modules/parent/mappers/parent-dashboard-calendar.mapper";
import {
    createParentProfile,
    createParentShell,
} from "@/modules/parent/mappers/parent-dashboard-shell.mapper";
import type {
    ParentDashboardModel,
    ParentDashboardSummary,
} from "@/modules/parent/types/parent-dashboard.types";

export function createParentDashboardModel(
    fullName = "",
    summary?: ParentDashboardSummary,
): ParentDashboardModel {
    const profile = createParentProfile(fullName, summary);
    const dayCard = createParentDayCard(summary);
    const miniPlan = createParentMiniPlan(summary);

    return {
        shell: createParentShell(profile),
        hero: parentDashboardHero,
        dayCard,
        miniPlan,
        heroSection: {
            hero: parentDashboardHero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайшее расписание",
            miniPlanIcon: "fas fa-clock",
        },
        calendarContent: createParentCalendarContent(summary),
        calendarDays: summary?.calendar.days ?? createEmptyParentCalendarDays(),
        createModal: parentCreateModalContent,
        notifications: {
            title: "Уведомления",
            createLabel: "Создать уведомление",
            items: summary?.notifications ?? [],
            emptyText: "Уведомлений пока нет.",
            actionLabel: "Посмотреть все уведомления",
            actionTo: { name: "parent-notifications" },
        },
        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            removeLabel: "Удалить заметку",
            items: summary?.notes ?? [],
            emptyText: "Заметок пока нет.",
            actionLabel: "Открыть все заметки",
            actionTo: { name: "parent-notes" },
        },
        profilePanel: {
            user: profile,
            title: "Профиль родителя",
            subtitle: "Доступ к учебному контролю и настройкам кабинета",
            actions: [
                { label: "Мой профиль", icon: "fas fa-user", to: { name: "parent-profile" } },
                { label: "Настройки", icon: "fas fa-gear", to: { name: "parent-settings" } },
                { label: "Выйти", icon: "fas fa-arrow-right-from-bracket", action: "logout" },
            ],
        },
        stats: summary?.stats ?? createEmptyParentStats(),
        scheduleSection: parentDashboardSections.schedule,
        schedule: summary?.schedule ?? [],
        notificationsSection: parentDashboardSections.notifications,
        importantItems: summary?.importantItems ?? [],
        coursesSection: parentDashboardSections.courses,
        courses: summary?.courses ?? [],
        activitySection: parentDashboardSections.activity,
        activityItems: summary?.activityItems ?? [],
        gradesSection: parentDashboardSections.grades,
        gradeRows: summary?.gradeRows ?? [],
        messagesSection: parentDashboardSections.messages,
        messages: summary?.messages ?? [],
    };
}
