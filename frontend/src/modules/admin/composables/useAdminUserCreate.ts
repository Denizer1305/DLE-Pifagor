import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { formatRussianPhone, normalizeRussianPhone } from "@/modules/auth/composables/usePhoneMask";
import { adminUserCreateContent } from "@/modules/admin/data/admin-users.data";
import { createAdminUserCreateForm } from "@/modules/admin/mappers/admin-users.mapper";
import { createAdminUser } from "@/modules/admin/services/admin-users.service";

export function useAdminUserCreate() {
    const router = useRouter();
    const form = reactive(createAdminUserCreateForm());
    const isSaving = ref(false);
    const errorMessage = ref("");
    const saveMessage = ref("");

    function handlePhoneInput(event: Event): void {
        const input = event.target as HTMLInputElement;

        form.phone = formatRussianPhone(input.value);
    }

    async function submit(): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";
        saveMessage.value = "";

        try {
            form.phone = normalizeRussianPhone(form.phone);
            const user = await createAdminUser(form);

            saveMessage.value = adminUserCreateContent.successMessage;
            await router.push({
                name: "admin-user-detail",
                params: { id: user.id },
            });
        } catch (error) {
            form.phone = formatRussianPhone(form.phone);
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось создать пользователя.";
        } finally {
            isSaving.value = false;
        }
    }

    return {
        errorMessage,
        form,
        isSaving,
        saveMessage,
        handlePhoneInput,
        submit,
    };
}
