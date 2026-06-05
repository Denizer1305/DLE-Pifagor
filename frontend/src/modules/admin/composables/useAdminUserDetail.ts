import { ref } from "vue";
import { useRoute } from "vue-router";

import { adminUserDetailContent } from "@/modules/admin/data/admin-users.data";
import {
    getAdminUserDetail,
    updateAdminUserStatus,
} from "@/modules/admin/services/admin-users.service";
import type {
    AdminUserDetailModel,
    AdminUserStatusAction,
} from "@/modules/admin/types/admin-users.types";

export function useAdminUserDetail() {
    const route = useRoute();
    const user = ref<AdminUserDetailModel | null>(null);
    const isLoading = ref(false);
    const updatingAction = ref<AdminUserStatusAction | null>(null);
    const errorMessage = ref("");

    const userId = Number(route.params.id);

    async function loadUser(): Promise<void> {
        if (!userId) {
            errorMessage.value = "Пользователь не найден.";
            return;
        }

        isLoading.value = true;
        errorMessage.value = "";

        try {
            user.value = await getAdminUserDetail(userId);
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось загрузить пользователя.";
        } finally {
            isLoading.value = false;
        }
    }

    async function runStatusAction(action: AdminUserStatusAction): Promise<void> {
        if (!user.value) {
            return;
        }

        updatingAction.value = action;
        errorMessage.value = "";

        try {
            user.value = await updateAdminUserStatus(
                user.value.id,
                action,
                user.value.expectedUpdatedAt,
            );
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось обновить статус пользователя.";
        } finally {
            updatingAction.value = null;
        }
    }

    return {
        content: adminUserDetailContent,
        errorMessage,
        isLoading,
        updatingAction,
        user,
        loadUser,
        runStatusAction,
    };
}
