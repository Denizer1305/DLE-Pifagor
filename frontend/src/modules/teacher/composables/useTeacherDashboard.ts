import { computed, onMounted, ref } from "vue";

import {
    createEmptyTeacherDashboardPageModel,
    createEmptyTeacherDashboardSummary,
    createEmptyTeacherDashboardViewModel,
} from "@/modules/teacher/data/teacher-dashboard-initial-state.data";
import { getTeacherDashboard } from "@/modules/teacher/services/teacher-dashboard.service";
import type {
    TeacherDashboardPageModel,
    TeacherDashboardSummary,
    TeacherDashboardViewModel,
} from "@/modules/teacher/types/teacher-dashboard.types";

function getErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить кабинет преподавателя.";
}

export function useTeacherDashboard() {
    const summary = ref<TeacherDashboardSummary>(createEmptyTeacherDashboardSummary());
    const pageModel = ref<TeacherDashboardPageModel>(createEmptyTeacherDashboardPageModel());
    const viewModel = ref<TeacherDashboardViewModel>(createEmptyTeacherDashboardViewModel());

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
