import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { adminUserEditContent } from "@/modules/admin/data/admin-users.data";
import {
    getAdminUserForEdit,
    saveAdminUserEdit,
} from "@/modules/admin/services/admin-users.service";
import type {
    AdminUserDetailModel,
    AdminUserEditForm,
} from "@/modules/admin/types/admin-users.types";

function createEmptyForm(): AdminUserEditForm {
    return {
        email: "",
        backupEmail: "",
        phone: "",
        firstName: "",
        lastName: "",
        middleName: "",
        birthDate: "",
        isLoginAllowed: true,
        reason: "",
    };
}

export function useAdminUserEdit() {
    const route = useRoute();
    const router = useRouter();
    const form = reactive<AdminUserEditForm>(createEmptyForm());
    const user = ref<AdminUserDetailModel | null>(null);
    const isLoading = ref(false);
    const isSaving = ref(false);
    const errorMessage = ref("");
    const saveMessage = ref("");

    const userId = Number(route.params.id);

    async function loadUser(): Promise<void> {
        if (!userId) {
            errorMessage.value = "Пользователь не найден.";
            return;
        }

        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getAdminUserForEdit(userId);
            Object.assign(form, result.form);
            user.value = result.model;
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось загрузить пользователя.";
        } finally {
            isLoading.value = false;
        }
    }

    async function submit(): Promise<void> {
        if (!user.value) {
            return;
        }

        isSaving.value = true;
        errorMessage.value = "";
        saveMessage.value = "";

        try {
            user.value = await saveAdminUserEdit(
                user.value.id,
                form,
                user.value.expectedUpdatedAt,
            );
            saveMessage.value = "Изменения сохранены.";
            await router.push({
                name: "admin-user-detail",
                params: { id: user.value.id },
            });
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось сохранить изменения.";
        } finally {
            isSaving.value = false;
        }
    }

    return {
        content: adminUserEditContent,
        errorMessage,
        form,
        isLoading,
        isSaving,
        saveMessage,
        user,
        loadUser,
        submit,
    };
}
