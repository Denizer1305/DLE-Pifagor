import { computed, onMounted, ref } from "vue";

import { teacherCreateModalContent } from "@/modules/teacher/data/teacher-dashboard.data";
import { getTeacherDashboard } from "@/modules/teacher/services/teacher-dashboard.service";
import type {
    TeacherDashboardPageModel,
    TeacherDashboardSummary,
    TeacherDashboardViewModel,
} from "@/modules/teacher/types/teacher-dashboard.types";

const dashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

function createEmptySummary(): TeacherDashboardSummary {
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

function createEmptyPageModel(): TeacherDashboardPageModel {
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

function createEmptyViewModel(): TeacherDashboardViewModel {
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

function getErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить кабинет преподавателя.";
}

export function useTeacherDashboard() {
    const summary = ref<TeacherDashboardSummary>(createEmptySummary());
    const pageModel = ref<TeacherDashboardPageModel>(createEmptyPageModel());
    const viewModel = ref<TeacherDashboardViewModel>(createEmptyViewModel());

    const isLoading = ref(false);
    const errorMessage = ref("");

    const hasDashboard = computed(() => {
        return Boolean(summary.value.profile.id);
    });

    async function loadDashboard(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getTeacherDashboard();

            summary.value = result.summary;
            pageModel.value = result.pageModel;
            viewModel.value = result.viewModel;
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    onMounted(() => {
        void loadDashboard();
    });

    return {
        summary,
        pageModel,
        viewModel,
        isLoading,
        errorMessage,
        hasDashboard,
        loadDashboard,
    };
}
