import { computed, ref, type Ref } from "vue";

import { createParentDashboardModel } from "@/modules/parent/data/parent-dashboard.data";
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

    function loadDashboard(): void {
        summary.value = null;
        errorMessage.value = "";
    }

    return {
        summary,
        model,
        isLoading,
        errorMessage,
        loadDashboard,
    };
}
