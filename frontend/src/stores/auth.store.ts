import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { setAccessToken } from "@/services/api/http.client";
import * as authApi from "@/modules/auth/api/auth.api";
import { getCurrentUser } from "@/modules/users/api/users.api";
import { getCurrentUserSettings } from "@/modules/users/api/user-settings.api";
import type {
    GuardianRegistrationPayload,
    LearnerRegistrationPayload,
    LoginPayload,
    MinorLearnerRegistrationPayload,
    TeacherRegistrationPayload,
} from "@/modules/auth/types/auth.types";
import type { RoleCode } from "@/app/constants/roles.constants";
import type { UserSettings } from "@/modules/users/types/user-settings.types";
import type { UserDetail } from "@/modules/users/types/user.types";

let initAuthPromise: Promise<void> | null = null;

export const useAuthStore = defineStore("auth", () => {
    const user = ref<UserDetail | null>(null);
    const settings = ref<UserSettings | null>(null);

    const isLoading = ref(false);
    const isInitialized = ref(false);
    const errorMessage = ref<string | null>(null);

    const isAuthenticated = computed(() => Boolean(user.value));
    const activeRole = computed<RoleCode | "">(() => settings.value?.active_role || "");

    const userFullName = computed(() => {
        if (!user.value) {
            return "";
        }

        return user.value.full_name || `${user.value.last_name} ${user.value.first_name}`.trim();
    });

    const isEmailVerified = computed(() => Boolean(user.value?.is_email_verified));
    const isLoginAllowed = computed(() => Boolean(user.value?.is_login_allowed));

    function resetAuthState(): void {
        setAccessToken(null);
        user.value = null;
        settings.value = null;
    }

    async function loadUserContext(): Promise<void> {
        const [currentUser, currentSettings] = await Promise.all([
            getCurrentUser(),
            getCurrentUserSettings(),
        ]);

        user.value = currentUser;
        settings.value = currentSettings;
    }

    async function initAuth(): Promise<void> {
        if (isInitialized.value) {
            return;
        }

        if (initAuthPromise) {
            return initAuthPromise;
        }

        initAuthPromise = (async () => {
            isLoading.value = true;
            errorMessage.value = null;

            try {
                const refreshResponse = await authApi.refresh();

                setAccessToken(refreshResponse.access);

                await loadUserContext();
            } catch {
                resetAuthState();
            } finally {
                isInitialized.value = true;
                isLoading.value = false;
                initAuthPromise = null;
            }
        })();

        return initAuthPromise;
    }

    async function login(payload: LoginPayload): Promise<void> {
        isLoading.value = true;
        errorMessage.value = null;

        try {
            const response = await authApi.login(payload);

            setAccessToken(response.access);
            user.value = response.user;

            settings.value = await getCurrentUserSettings();
            isInitialized.value = true;
        } catch (error) {
            resetAuthState();

            if (error instanceof Error) {
                errorMessage.value = error.message;
            } else {
                errorMessage.value = "Не удалось выполнить вход.";
            }

            throw error;
        } finally {
            isLoading.value = false;
        }
    }

    async function logout(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = null;

        try {
            await authApi.logout();
        } finally {
            resetAuthState();
            isInitialized.value = true;
            isLoading.value = false;
        }
    }

    async function reloadCurrentUser(): Promise<void> {
        if (!isAuthenticated.value) {
            return;
        }

        isLoading.value = true;
        errorMessage.value = null;

        try {
            await loadUserContext();
        } catch (error) {
            if (error instanceof Error) {
                errorMessage.value = error.message;
            } else {
                errorMessage.value = "Не удалось обновить данные пользователя.";
            }

            throw error;
        } finally {
            isLoading.value = false;
        }
    }

    async function refreshSession(): Promise<boolean> {
        try {
            const response = await authApi.refresh();

            setAccessToken(response.access);
            await loadUserContext();

            isInitialized.value = true;

            return true;
        } catch {
            resetAuthState();
            isInitialized.value = true;

            return false;
        }
    }

    async function registerTeacher(payload: TeacherRegistrationPayload): Promise<UserDetail> {
        return authApi.registerTeacher(payload);
    }

    async function registerLearner(payload: LearnerRegistrationPayload): Promise<UserDetail> {
        return authApi.registerLearner(payload);
    }

    async function registerGuardian(payload: GuardianRegistrationPayload): Promise<UserDetail> {
        return authApi.registerGuardian(payload);
    }

    async function registerMinorLearner(payload: MinorLearnerRegistrationPayload): Promise<UserDetail> {
        return authApi.registerMinorLearner(payload);
    }

    function hasRole(roleCode: RoleCode): boolean {
        return activeRole.value === roleCode;
    }

    function hasAnyRole(roleCodes: RoleCode[]): boolean {
        if (!activeRole.value) {
            return false;
        }

        return roleCodes.includes(activeRole.value);
    }

    return {
        user,
        settings,
        isLoading,
        isInitialized,
        errorMessage,

        isAuthenticated,
        activeRole,
        userFullName,
        isEmailVerified,
        isLoginAllowed,

        initAuth,
        login,
        logout,
        reloadCurrentUser,
        refreshSession,
        resetAuthState,

        registerTeacher,
        registerLearner,
        registerGuardian,
        registerMinorLearner,

        hasRole,
        hasAnyRole,
    };
});
