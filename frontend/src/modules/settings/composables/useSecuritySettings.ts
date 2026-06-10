import { computed, onMounted, reactive, ref } from "vue";

import { ROLE_LABELS } from "@/app/constants/roles.constants";
import {
    getSecuritySessions,
    getSecuritySettings,
    logoutAllSessions,
    logoutSession,
    savePassword,
    saveSecuritySettings,
} from "@/modules/settings/services/settings.service";
import { mapSecuritySettingsToPageState } from "@/modules/settings/mappers/settings.mapper";
import type {
    PasswordFormErrors,
    PasswordFormState,
    SecuritySessionsDto,
    SecuritySettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import { useAuthStore } from "@/stores/auth.store";
import { useLocaleStore } from "@/stores/locale.store";

function createPasswordForm(): PasswordFormState {
    return {
        currentPassword: "",
        newPassword: "",
        newPasswordConfirm: "",
    };
}

function createPasswordErrors(): PasswordFormErrors {
    return {
        currentPassword: "",
        newPassword: "",
        newPasswordConfirm: "",
        common: "",
    };
}

export function useSecuritySettings() {
    const authStore = useAuthStore();
    const localeStore = useLocaleStore();

    const settings = ref<SecuritySettingsDto | null>(null);
    const sessions = ref<SecuritySessionsDto | null>(null);
    const pageState = ref<SettingsPageState<SecuritySettingsDto> | null>(null);

    const passwordForm = reactive<PasswordFormState>(createPasswordForm());
    const passwordErrors = reactive<PasswordFormErrors>(createPasswordErrors());

    const isLoading = ref(false);
    const isSaving = ref(false);
    const isPasswordSubmitting = ref(false);
    const errorMessage = ref("");
    const successMessage = ref("");

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

    async function loadSecuritySettings(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const [settingsResult, sessionsResult] = await Promise.all([
                getSecuritySettings(),
                getSecuritySessions(),
            ]);

            setSettings(settingsResult);
            sessions.value = sessionsResult;
        } catch (error) {
            errorMessage.value = getSecurityErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    async function updateSecurity(
        payload: Partial<SecuritySettingsDto>,
    ): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";

        try {
            const result = await saveSecuritySettings(payload);

            setSettings(result);
        } catch (error) {
            errorMessage.value = getSecurityErrorMessage(error);
        } finally {
            isSaving.value = false;
        }
    }

    async function submitPasswordChange(): Promise<void> {
        clearPasswordErrors();

        if (!validatePasswordForm()) {
            return;
        }

        isPasswordSubmitting.value = true;
        successMessage.value = "";

        try {
            const response = await savePassword({
                current_password: passwordForm.currentPassword,
                new_password: passwordForm.newPassword,
                new_password_confirm: passwordForm.newPasswordConfirm,
            });

            Object.assign(passwordForm, createPasswordForm());
            successMessage.value = response.detail;
        } catch (error) {
            passwordErrors.common = getSecurityErrorMessage(error);
        } finally {
            isPasswordSubmitting.value = false;
        }
    }

    async function logoutAllUserSessions(): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";

        try {
            const response = await logoutAllSessions();

            successMessage.value = response.detail;
            sessions.value = await getSecuritySessions();
        } catch (error) {
            errorMessage.value = getSecurityErrorMessage(error);
        } finally {
            isSaving.value = false;
        }
    }

    async function logoutUserSession(sessionId: string): Promise<void> {
        isSaving.value = true;
        errorMessage.value = "";

        try {
            const response = await logoutSession(sessionId);

            successMessage.value = response.detail;
            sessions.value = await getSecuritySessions();
        } catch (error) {
            errorMessage.value = getSecurityErrorMessage(error);
        } finally {
            isSaving.value = false;
        }
    }

    function setSettings(nextSettings: SecuritySettingsDto): void {
        settings.value = nextSettings;
        pageState.value = mapSecuritySettingsToPageState(
            nextSettings,
            userContext.value,
            localeStore.locale,
        );
    }

    function clearPasswordErrors(): void {
        Object.assign(passwordErrors, createPasswordErrors());
    }

    function validatePasswordForm(): boolean {
        if (!passwordForm.currentPassword.trim()) {
            passwordErrors.currentPassword = "Укажите текущий пароль.";
        }

        if (!passwordForm.newPassword.trim()) {
            passwordErrors.newPassword = "Укажите новый пароль.";
        }

        if (passwordForm.newPassword !== passwordForm.newPasswordConfirm) {
            passwordErrors.newPasswordConfirm = "Пароли не совпадают.";
        }

        return !passwordErrors.currentPassword &&
            !passwordErrors.newPassword &&
            !passwordErrors.newPasswordConfirm;
    }

    onMounted(() => {
        void loadSecuritySettings();
    });

    return {
        settings,
        sessions,
        pageState,
        passwordForm,
        passwordErrors,
        isLoading,
        isSaving,
        isPasswordSubmitting,
        errorMessage,
        successMessage,
        loadSecuritySettings,
        updateSecurity,
        submitPasswordChange,
        logoutAllUserSessions,
        logoutUserSession,
    };
}

function getSecurityErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить настройки безопасности.";
}
