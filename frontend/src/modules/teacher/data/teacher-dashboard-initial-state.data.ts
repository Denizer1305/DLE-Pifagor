import { dashboardTopbarLabels } from "@/components/dashboard/mappers/dashboard-shell.mapper";
import { teacherCreateModalContent } from "@/modules/teacher/data/teacher-dashboard.data";
import type {
    TeacherDashboardPageModel,
    TeacherDashboardSummary,
    TeacherDashboardViewModel,
} from "@/modules/teacher/types/teacher-dashboard.types";

export function createEmptyTeacherDashboardSummary(): TeacherDashboardSummary {
    return {
        profile: {
            id: 0,
            fullName: "",
            email: "",
            avatarUrl: "",
            roleLabel: "",
            subjectLabel: "",
        },
        stats: [],
        schedule: [],
        calendar: {
            monthLabel: "",
            selectedDate: "",
            days: [],
        },
        courses: [],
        attentionItems: [],
        activityItems: [],
        journalRows: [],
        notifications: [],
        notes: [],
    };
}

export function createEmptyTeacherDashboardPageModel(): TeacherDashboardPageModel {
    const hero = {
        badges: [],
        title: "",
        text: "",
        actions: [],
    };
    const dayCard = {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: "",
        text: "",
        stats: [],
    };
    const miniPlan: TeacherDashboardPageModel["miniPlan"] = [];

    return {
        hero,
        dayCard,
        miniPlan,
        heroSection: {
            hero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайшее расписание",
            miniPlanIcon: "fas fa-clock",
        },
        featuredStat: {
            icon: "",
            title: "",
            value: "",
            label: "",
            progress: 0,
        },
        compactStats: [],
        planItems: [],
        attentionItems: [],
        courses: [],
        activityItems: [],
        journalRows: [],
        ai: {
            image: {
                src: "",
                alt: "",
            },
            title: "",
            subtitle: "",
            text: "",
            action: {
                label: "",
                to: {
                    name: "teacher-dashboard",
                },
            },
        },
    };
}

export function createEmptyTeacherDashboardViewModel(): TeacherDashboardViewModel {
    return {
        shell: {
            pageClass: "teacher-dashboard-page",
            role: "teacher",
            brand: {
                logo: "",
                title: "",
                subtitle: "",
            },
            profile: {
                fullName: "",
                roleLabel: "",
                avatarAlt: "",
            },
            navigation: [],
            search: {
                placeholder: "",
                ariaLabel: "",
            },
            topbarLabels: dashboardTopbarLabels,
            topbarUser: {
                fullName: "",
                roleLabel: "",
                avatarAlt: "",
            },
        },
        calendarContent: {
            title: "",
            monthLabel: "",
            previousMonthLabel: "",
            nextMonthLabel: "",
            weekdays: [],
        },
        calendarDays: [],
        notifications: {
            title: "",
            items: [],
        },
        notes: {
            title: "",
            items: [],
        },
        profilePanel: {
            user: {
                fullName: "",
                roleLabel: "",
                avatarAlt: "",
            },
            title: "",
            subtitle: "",
            actions: [],
        },
        createModal: teacherCreateModalContent,
    };
}
