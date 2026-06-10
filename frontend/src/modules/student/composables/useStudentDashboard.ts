import { computed, onMounted, ref, type Ref } from "vue";

import { createStudentDashboardModel } from "@/modules/student/mappers/student-dashboard-page.mapper";
import { getStudentDashboard } from "@/modules/student/services/student-dashboard.service";
import type {
    StudentDashboardModel,
    StudentDashboardSummary,
} from "@/modules/student/types/student-dashboard.types";

function getErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить личный кабинет студента.";
}

export function useStudentDashboard(fallbackName: Ref<string>) {
    const summary = ref<StudentDashboardSummary | null>(null);
    const model = ref<StudentDashboardModel>(
        createStudentDashboardModel(fallbackName.value),
    );
    const isLoading = ref(false);
    const errorMessage = ref("");

    const hasDashboard = computed(() => {
        return Boolean(summary.value?.profile.id);
    });

    async function loadDashboard(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getStudentDashboard(fallbackName.value);

            summary.value = result.summary;
            model.value = result.model;
        } catch (error) {
            errorMessage.value = getErrorMessage(error);
            model.value = createStudentDashboardModel(fallbackName.value);
        } finally {
            isLoading.value = false;
        }
    }

    onMounted(() => {
        void loadDashboard();
    });

    return {
        summary,
        model,
        isLoading,
        errorMessage,
        hasDashboard,
        loadDashboard,
    };
}
