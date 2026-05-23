import { computed, ref } from "vue";
import { defineStore } from "pinia";

import {
    clearAccessToken,
    getAccessToken,
    refreshAccessToken,
    setAccessToken,
} from "@/services/api/http.client";
import * as authApi from "@/modules/auth/api/auth.api";
import { getCurrentUser } from "@/modules/users/api/users.api";
import { fetchCurrentProfile } from "@/modules/profile/api/profile.api";
import {
    getCurrentUserSettings,
    setActiveRole,
} from "@/modules/users/api/user-settings.api";
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
import { ROLE_CODES } from "@/app/constants/roles.constants";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

let initAuthPromise: Promise<void> | null = null;

const ROLE_AUTO_DETECT_ORDER: RoleCode[] = [
    ROLE_CODES.SUPERADMIN,
    ROLE_CODES.PLATFORM_ADMIN,
    ROLE_CODES.ADMIN,
    ROLE_CODES.DIRECTOR,
    ROLE_CODES.ORG_ADMIN,
    ROLE_CODES.DEPARTMENT_HEAD,
    ROLE_CODES.TEACHER,
    ROLE_CODES.CURATOR,
    ROLE_CODES.METHODIST,
    ROLE_CODES.ORGANIZER,
    ROLE_CODES.MENTOR,
    ROLE_CODES.LEARNER,
    ROLE_CODES.GUARDIAN,
];

export const useAuthStore = defineStore("auth", () => {
    const user = ref<UserDetail | null>(null);
    const settings = ref<UserSettings | null>(null);
    const avatarUrl = ref("");

    const isLoading = ref(false);
    const isInitialized = ref(false);
    const errorMessage = ref<string | null>(null);

    const isAuthenticated = computed(() => Boolean(user.value));
    const activeRole = computed<RoleCode | "">(() => settings.value?.active_role || "");
    const isSuperuser = computed(() => Boolean(user.value?.is_superuser));

    const userFullName = computed(() => {
        if (!user.value) {
            return "";
        }

        return user.value.full_name || `${user.value.last_name} ${user.value.first_name}`.trim();
    });

    const isEmailVerified = computed(() => Boolean(user.value?.is_email_verified));
    const isLoginAllowed = computed(() => Boolean(user.value?.is_login_allowed));

    function resetAuthState(): void {
        clearAccessToken();
        user.value = null;
        settings.value = null;
        avatarUrl.value = "";
    }

    async function loadUserContext(): Promise<void> {
        const [currentUser, currentSettings, currentProfile] = await Promise.all([
            getCurrentUser(),
            getCurrentUserSettings(),
            fetchCurrentProfile().catch(() => null),
        ]);

        user.value = currentUser;
        avatarUrl.value = resolveBackendAssetUrl(
            currentProfile?.identity.avatar_url,
        );
        settings.value = currentSettings.active_role
            ? currentSettings
            : await resolveInitialUserRole(currentUser);
    }

    async function resolveInitialUserRole(
        currentUser: UserDetail,
    ): Promise<UserSettings> {
        if (currentUser.is_superuser) {
            return getCurrentUserSettings();
        }

        const availableRoles = currentUser.active_roles || [];
        const orderedAvailableRoles = ROLE_AUTO_DETECT_ORDER.filter((roleCode) => {
            return availableRoles.includes(roleCode);
        });

        for (const roleCode of orderedAvailableRoles) {
            try {
                return await setActiveRole({
                    role_code: roleCode,
                });
            } catch {
                continue;
            }
        }

        return getCurrentUserSettings();
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
                const savedAccessToken = getAccessToken();

                if (!savedAccessToken) {
                    const refreshedAccessToken = await refreshAccessToken();

                    if (!refreshedAccessToken) {
                        resetAuthState();
                        return;
                    }
                }

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
            const currentProfile = await fetchCurrentProfile().catch(() => null);
            avatarUrl.value = resolveBackendAssetUrl(
                currentProfile?.identity.avatar_url,
            );
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
        isLoading.value = true;
        errorMessage.value = null;

        try {
            const access = await refreshAccessToken();

            if (!access) {
                resetAuthState();
                isInitialized.value = true;

                return false;
            }

            await loadUserContext();

            isInitialized.value = true;

            return true;
        } catch {
            resetAuthState();
            isInitialized.value = true;

            return false;
        } finally {
            isLoading.value = false;
        }
    }

    function setAvatarUrl(value: string): void {
        avatarUrl.value = resolveBackendAssetUrl(value);
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
        avatarUrl,
        isLoading,
        isInitialized,
        errorMessage,

        isAuthenticated,
        activeRole,
        isSuperuser,
        userFullName,
        isEmailVerified,
        isLoginAllowed,

        initAuth,
        login,
        logout,
        reloadCurrentUser,
        refreshSession,
        resetAuthState,
        setAvatarUrl,

        registerTeacher,
        registerLearner,
        registerGuardian,
        registerMinorLearner,

        hasRole,
        hasAnyRole,
    };
});
