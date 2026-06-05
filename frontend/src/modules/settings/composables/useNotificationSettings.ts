import { computed, onMounted, ref } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import {
    getNotificationSettings,
    saveNotificationSettings,
} from "@/modules/settings/services/settings.service";
import { mapNotificationSettingsToPageState } from "@/modules/settings/mappers/settings.mapper";
import type {
    NotificationSettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import { useAuthStore } from "@/stores/auth.store";
import { useLocaleStore } from "@/stores/locale.store";

export function useNotificationSettings() {
    const authStore = useAuthStore();
    const localeStore = useLocaleStore();

    const settings = ref<NotificationSettingsDto | null>(null);
    const pageState = ref<SettingsPageState<NotificationSettingsDto> | null>(null);

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

    async function loadNotificationSettings(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getNotificationSettings();

            setSettings(result);
        } catch (error) {
            errorMessage.value = getNotificationErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    async function updateNotifications(
        payload: Partial<NotificationSettingsDto>,
    ): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";

        try {
            const result = await saveNotificationSettings(payload);

            setSettings(result);
        } catch (error) {
            errorMessage.value = getNotificationErrorMessage(error);
        } finally {
            isSaving.value = false;
        }
    }

    function setSettings(nextSettings: NotificationSettingsDto): void {
        settings.value = nextSettings;
        pageState.value = mapNotificationSettingsToPageState(
            nextSettings,
            userContext.value,
            localeStore.locale,
        );
    }

    onMounted(() => {
        void loadNotificationSettings();
    });

    return {
        settings,
        pageState,
        isLoading,
        isSaving,
        errorMessage,
        loadNotificationSettings,
        updateNotifications,
    };
}

function getNotificationErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить настройки уведомлений.";
}
