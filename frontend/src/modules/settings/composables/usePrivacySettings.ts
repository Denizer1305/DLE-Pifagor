import { computed, onMounted, ref } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import {
    getPrivacySettings,
    savePrivacySettings,
} from "@/modules/settings/services/settings.service";
import { mapPrivacySettingsToPageState } from "@/modules/settings/mappers/settings.mapper";
import type {
    PrivacySettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import { useAuthStore } from "@/stores/auth.store";
import { useLocaleStore } from "@/stores/locale.store";

export function usePrivacySettings() {
    const authStore = useAuthStore();
    const localeStore = useLocaleStore();

    const settings = ref<PrivacySettingsDto | null>(null);
    const pageState = ref<SettingsPageState<PrivacySettingsDto> | null>(null);

    const isLoading = ref(false);
    const isSaving = ref(false);
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

    async function loadPrivacySettings(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getPrivacySettings();

            setSettings(result);
        } catch (error) {
            errorMessage.value = getPrivacyErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    async function updatePrivacy(
        payload: Partial<PrivacySettingsDto>,
    ): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";

        try {
            const result = await savePrivacySettings(payload);

            setSettings(result);
        } catch (error) {
            errorMessage.value = getPrivacyErrorMessage(error);
        } finally {
            isSaving.value = false;
        }
    }

    function setSettings(nextSettings: PrivacySettingsDto): void {
        settings.value = nextSettings;
        pageState.value = mapPrivacySettingsToPageState(
            nextSettings,
            userContext.value,
            localeStore.locale,
        );
    }

    onMounted(() => {
        void loadPrivacySettings();
    });

    return {
        settings,
        pageState,
        isLoading,
        isSaving,
        errorMessage,
        loadPrivacySettings,
        updatePrivacy,
    };
}

function getPrivacyErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить настройки приватности.";
}
