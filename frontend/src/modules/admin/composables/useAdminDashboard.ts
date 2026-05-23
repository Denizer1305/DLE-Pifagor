import { computed, onMounted, ref, watch } from "vue";

import { getAdminDashboardSummary } from "@/modules/admin/services/admin-dashboard.service";
import {
    mapAdminStatsToDashboardCards,
    mapAuditEventsToTimeline,
    mapFeedbackRequestsToSection,
    mapJoinRequestsToSection,
    mapRecentUsersToSection,
    mapSystemHealthToSection,
} from "@/modules/admin/mappers/admin-dashboard.mapper";
import { mapAdminSummaryToPageModel } from "@/modules/admin/mappers/admin-dashboard-page.mapper";
import {
    adminAiCardContent,
    adminDayCardContent,
    adminIntroContent,
    createAdminCalendarContent,
    adminCreateModalContent,
    createAdminNotificationsContent,
    createAdminNotesContent,
    createAdminProfilePanelContent,
    createAdminShellConfig,
} from "@/modules/admin/data/admin-dashboard.data";
import { useAuthStore } from "@/stores/auth.store";
import type {
    AdminDashboardSummary,
    AdminDashboardViewModel,
} from "@/modules/admin/types/admin-dashboard.types";

function createEmptyDashboard(): AdminDashboardSummary {
    return {
        profile: {
            id: 0,
            fullName: "",
            email: "",
            avatarUrl: "",
            roleLabel: "",
        },
        stats: [],
        calendar: {
            monthLabel: "",
            selectedDate: "",
            days: [],
        },
        recentUsers: [],
        joinRequests: [],
        feedbackRequests: [],
        auditEvents: [],
        systemHealth: {
            status: "ok",
            checks: [],
        },
        quickActions: [],
    };
}

function getErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить административную сводку.";
}

export function useAdminDashboard() {
    const authStore = useAuthStore();

    const dashboard = ref<AdminDashboardSummary>(createEmptyDashboard());
    const isDashboardRequestLoading = ref(false);
    const errorMessage = ref("");
    const hasLoaded = ref(false);

    const canLoadDashboard = computed(() => {
        return Boolean(
            authStore.isInitialized &&
            authStore.isAuthenticated &&
            authStore.user,
        );
    });

    const resolvedProfile = computed(() => {
        if (dashboard.value.profile.id) {
            return dashboard.value.profile;
        }

        const user = authStore.user;

        return {
            id: user?.id || 0,
            fullName: authStore.userFullName || user?.email || "",
            email: user?.email || "",
            avatarUrl: "",
            roleLabel: getAuthRoleLabel(),
        };
    });

    const viewModel = computed<AdminDashboardViewModel>(() => {
        return {
            shell: createAdminShellConfig(
                resolvedProfile.value,
                dashboard.value.stats,
            ),
            calendarContent: createAdminCalendarContent(
                dashboard.value.calendar.monthLabel,
            ),
            calendarDays: dashboard.value.calendar.days,
            notifications: createAdminNotificationsContent(),
            notes: createAdminNotesContent(),
            profilePanel: createAdminProfilePanelContent(
                resolvedProfile.value,
            ),
            createModal: adminCreateModalContent,
            intro: adminIntroContent,
            dayCard: adminDayCardContent,
            stats: mapAdminStatsToDashboardCards(dashboard.value.stats),
            quickActions: dashboard.value.quickActions,
            recentUsers: mapRecentUsersToSection(dashboard.value.recentUsers),
            joinRequests: mapJoinRequestsToSection(dashboard.value.joinRequests),
            feedbackRequests: mapFeedbackRequestsToSection(
                dashboard.value.feedbackRequests,
            ),
            audit: mapAuditEventsToTimeline(dashboard.value.auditEvents),
            systemHealth: mapSystemHealthToSection(dashboard.value.systemHealth),
            ai: adminAiCardContent,
        };
    });

    const pageModel = computed(() => {
        return mapAdminSummaryToPageModel(dashboard.value);
    });

    const hasStats = computed(() => {
        return dashboard.value.stats.length > 0;
    });

    async function loadDashboard(): Promise<void> {
        if (!canLoadDashboard.value) {
            return;
        }

        isDashboardRequestLoading.value = true;
        errorMessage.value = "";

        try {
            dashboard.value = await getAdminDashboardSummary();
            hasLoaded.value = true;
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
        } finally {
            isDashboardRequestLoading.value = false;
        }
    }

    const isLoading = computed(() => {
        return !authStore.isInitialized || isDashboardRequestLoading.value;
    });

    function getAuthRoleLabel(): string {
        if (authStore.isSuperuser) {
            return "Суперпользователь платформы";
        }

        if (authStore.activeRole) {
            return authStore.activeRole;
        }

        return "";
    }

    onMounted(() => {
        if (canLoadDashboard.value) {
            void loadDashboard();
        }
    });

    watch(
        canLoadDashboard,
        (canLoad) => {
            if (canLoad && !hasLoaded.value) {
                void loadDashboard();
            }
        },
        {
            immediate: true,
        },
    );

    return {
        dashboard,
        errorMessage,
        hasStats,
        isLoading,
        loadDashboard,
        pageModel,
        viewModel,
    };
}
