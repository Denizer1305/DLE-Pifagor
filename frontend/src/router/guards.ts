import type { RouteLocationNormalized } from "vue-router";

import type { RoleCode } from "@/app/constants/roles.constants";
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
