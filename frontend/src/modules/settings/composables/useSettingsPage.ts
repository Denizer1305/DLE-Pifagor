import { computed, onMounted, ref } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import { getUserSettings } from "@/modules/settings/services/settings.service";
import { mapUserSettingsToCenterModel } from "@/modules/settings/mappers/settings.mapper";
import type {
    SettingsCenterModel,
    UserSettingsDto,
} from "@/modules/settings/types/settings.types";
import { useAuthStore } from "@/stores/auth.store";
import { useLocaleStore } from "@/stores/locale.store";

export function useSettingsPage() {
    const authStore = useAuthStore();
    const localeStore = useLocaleStore();

    const settings = ref<UserSettingsDto | null>(null);
    const pageModel = ref<SettingsCenterModel | null>(null);

    const isLoading = ref(false);
    const errorMessage = ref("");

    const userContext = computed(() => {
        return {
            fullName: authStore.userFullName || "Пользователь",
            roleLabel: authStore.activeRole
                ? ROLE_LABELS[authStore.activeRole]
                : "Пользователь",
            roleCode: authStore.activeRole || "",
            avatarUrl: authStore.avatarUrl || "",
        };
    });

    async function loadSettings(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getUserSettings();

            settings.value = result;
            pageModel.value = mapUserSettingsToCenterModel(
                result,
                userContext.value,
                localeStore.locale,
            );
        } catch (error) {
            errorMessage.value = getSettingsErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    onMounted(() => {
        void loadSettings();
    });

    return {
        settings,
        pageModel,
        isLoading,
        errorMessage,
        loadSettings,
    };
}

function getSettingsErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить настройки пользователя.";
}
