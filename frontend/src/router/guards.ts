import type { RouteLocationNormalized } from "vue-router";

import { ROLE_CODES, type RoleCode } from "@/app/constants/roles.constants";
import { useAuthStore } from "@/stores/auth.store";
import { getDashboardRouteNameByRole } from "@/modules/auth/utils/auth-redirect.utils";

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

    if (authStore.isAuthenticated) {
        return {
            name: getDashboardRouteNameByRole(authStore.activeRole),
        };
    }

    return true;
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

        if (!authStore.hasAnyRole(allowedRoles)) {
            return {
                name: "forbidden",
            };
        }

        return true;
    };
}

export function getDefaultDashboardRouteName(roleCode: string): string {
    if (
        roleCode === ROLE_CODES.TEACHER ||
        roleCode === ROLE_CODES.CURATOR ||
        roleCode === ROLE_CODES.METHODIST ||
        roleCode === ROLE_CODES.ORGANIZER ||
        roleCode === ROLE_CODES.MENTOR
    ) {
        return "teacher-dashboard";
    }

    if (roleCode === ROLE_CODES.GUARDIAN) {
        return "parent-dashboard";
    }

    if (
        roleCode === ROLE_CODES.DIRECTOR ||
        roleCode === ROLE_CODES.ORG_ADMIN ||
        roleCode === ROLE_CODES.DEPARTMENT_HEAD ||
        roleCode === ROLE_CODES.SUPERADMIN
    ) {
        return "admin-dashboard";
    }

    return "student-dashboard";
}
