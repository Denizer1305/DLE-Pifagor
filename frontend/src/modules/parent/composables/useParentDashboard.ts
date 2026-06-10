import { computed, onMounted, ref, type Ref } from "vue";

import { createParentDashboardModel } from "@/modules/parent/mappers/parent-dashboard-page.mapper";
import { getParentDashboard } from "@/modules/parent/services/parent-dashboard.service";
import type {
    ParentDashboardModel,
    ParentDashboardSummary,
} from "@/modules/parent/types/parent-dashboard.types";

export function useParentDashboard(fallbackName: Ref<string>) {
    const summary = ref<ParentDashboardSummary | null>(null);
    const model = computed<ParentDashboardModel>(() => {
        return createParentDashboardModel(
            fallbackName.value,
            summary.value || undefined,
        );
    });

    const isLoading = ref(false);
    const errorMessage = ref("");

    async function loadDashboard(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            summary.value = await getParentDashboard();
        } catch (error) {
            errorMessage.value = error instanceof Error && error.message
                ? error.message
                : "Не удалось загрузить личный кабинет родителя.";
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
        loadDashboard,
    };
}
