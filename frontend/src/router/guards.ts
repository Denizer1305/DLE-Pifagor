import type { RouteLocationNormalized } from "vue-router";

import type { RoleCode } from "@/app/constants/roles.constants";
import { useAuthStore } from "@/stores/auth.store";
import {
    getDashboardRouteNameByRole,
    isAdminRole,
    isTeacherRole,
} from "@/modules/auth/utils/auth-redirect.utils";
import { ROLE_CODES } from "@/app/constants/roles.constants";

export async function authGuard(to: RouteLocationNormalized) {
    const authStore = useAuthStore();

    if (!authStore.isInitialized) {
        await authStore.initAuth();
    }

    if (!authStore.isAuthenticated) {
        return {
            name: "login",
            query: {
                redirect: to.fullPath,
            },
        };
    }

    return true;
}

export async function guestGuard() {
    const authStore = useAuthStore();

    if (!authStore.isInitialized) {
        await authStore.initAuth();
    }

    if (authStore.isAuthenticated && canRedirectToDashboard(
        authStore.activeRole,
        authStore.isSuperuser,
    )) {
        return {
            name: getDashboardRouteNameByRole(
                authStore.activeRole,
                authStore.isSuperuser,
            ),
        };
    }

    return true;
}

function canRedirectToDashboard(
    roleCode: RoleCode | "" | null | undefined,
    isSuperuser: boolean,
): boolean {
    return (
        isSuperuser ||
        isAdminRole(roleCode) ||
        isTeacherRole(roleCode) ||
        roleCode === ROLE_CODES.STUDENT ||
        roleCode === ROLE_CODES.LEARNER ||
        roleCode === ROLE_CODES.GUARDIAN
    );
}

export function roleGuard(allowedRoles: RoleCode[]) {
    return async (to: RouteLocationNormalized) => {
        const authStore = useAuthStore();

        if (!authStore.isInitialized) {
            await authStore.initAuth();
        }

        if (!authStore.isAuthenticated) {
            return {
                name: "login",
                query: {
                    redirect: to.fullPath,
                },
            };
        }

        const isAllowedSuperuser =
            authStore.isSuperuser &&
            allowedRoles.some((roleCode) => isAdminRole(roleCode));
        const isStudentOnboardingRoute =
            !authStore.activeRole &&
            Boolean(authStore.user) &&
            authStore.isEmailVerified &&
            authStore.isLoginAllowed &&
            (
                allowedRoles.includes(ROLE_CODES.LEARNER) ||
                allowedRoles.includes(ROLE_CODES.STUDENT)
            );

        if (
            !isAllowedSuperuser &&
            !isStudentOnboardingRoute &&
            !authStore.hasAnyRole(allowedRoles)
        ) {
            return {
                name: "forbidden",
            };
        }

        return true;
    };
}
