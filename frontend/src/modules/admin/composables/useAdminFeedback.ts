import { reactive, ref } from "vue";

import { adminFeedbackContent } from "@/modules/admin/data/admin-feedback.data";
import {
    getAdminFeedbackRequests,
    updateAdminFeedbackStatus,
} from "@/modules/admin/services/admin-feedback.service";
import type {
    AdminFeedbackFilters,
    AdminFeedbackList,
    AdminFeedbackStatus,
} from "@/modules/admin/types/admin-feedback.types";

function createEmptyList(): AdminFeedbackList {
    return {
        summary: { total: 0, new: 0, inProgress: 0, answered: 0, closed: 0 },
        items: [],
    };
}

export function useAdminFeedback() {
    const filters = reactive<AdminFeedbackFilters>({
        status: "",
        topic: "",
        search: "",
    });
    const feedback = ref<AdminFeedbackList>(createEmptyList());
    const isLoading = ref(false);
    const updatingId = ref<number | null>(null);
    const errorMessage = ref("");

    async function loadFeedback(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            feedback.value = await getAdminFeedbackRequests(filters);
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : adminFeedbackContent.errorText;
        } finally {
            isLoading.value = false;
        }
    }

    async function updateStatus(requestId: number, status: AdminFeedbackStatus): Promise<void> {
        updatingId.value = requestId;
        errorMessage.value = "";

        try {
            await updateAdminFeedbackStatus(requestId, status);
            await loadFeedback();
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось обновить статус обращения.";
        } finally {
            updatingId.value = null;
        }
    }

    return {
        filters,
        feedback,
        isLoading,
        updatingId,
        errorMessage,
        loadFeedback,
        updateStatus,
    };
}
