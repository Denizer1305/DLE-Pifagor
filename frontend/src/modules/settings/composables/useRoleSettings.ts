import { computed, onMounted, ref } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import {
    getRoleSettings,
    saveRoleSettings,
} from "@/modules/settings/services/settings.service";
import { mapRoleSettingsToPageState } from "@/modules/settings/mappers/settings.mapper";
import type {
    RoleSettingsDto,
    SettingsPageState,
    SettingsRoleCode,
} from "@/modules/settings/types/settings.types";
import { useAuthStore } from "@/stores/auth.store";
import { useLocaleStore } from "@/stores/locale.store";

export function useRoleSettings() {
    const authStore = useAuthStore();
    const localeStore = useLocaleStore();

    const settings = ref<RoleSettingsDto | null>(null);
    const pageState = ref<SettingsPageState<RoleSettingsDto> | null>(null);

    const isLoading = ref(false);
    const isSaving = ref(false);
    const errorMessage = ref("");

    const activeRole = computed(() => {
        return settings.value?.active_role || "teacher";
    });

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

    async function loadRoleSettings(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getRoleSettings();

            setSettings(result);
        } catch (error) {
            errorMessage.value = getRoleErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    async function setActiveRole(role: SettingsRoleCode): Promise<void> {
        await updateRoles({
            active_role: role,
        });
    }

    async function updateRoleOption(
        role: SettingsRoleCode,
        key: string,
        value: boolean,
    ): Promise<void> {
        if (!settings.value) {
            return;
        }

        await updateRoles({
            roles: {
                [role]: {
                    ...settings.value.roles[role],
                    [key]: value,
                },
            } as Partial<RoleSettingsDto["roles"]> as RoleSettingsDto["roles"],
        });
    }

    async function updateRoles(payload: Partial<RoleSettingsDto>): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";

        try {
            const result = await saveRoleSettings(payload);

            setSettings(result);
        } catch (error) {
            errorMessage.value = getRoleErrorMessage(error);
        } finally {
            isSaving.value = false;
        }
    }

    function setSettings(nextSettings: RoleSettingsDto): void {
        settings.value = nextSettings;
        pageState.value = mapRoleSettingsToPageState(
            nextSettings,
            userContext.value,
            localeStore.locale,
        );
    }

    onMounted(() => {
        void loadRoleSettings();
    });

    return {
        settings,
        pageState,
        activeRole,
        isLoading,
        isSaving,
        errorMessage,
        loadRoleSettings,
        setActiveRole,
        updateRoleOption,
        updateRoles,
    };
}

function getRoleErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить ролевые настройки.";
}
