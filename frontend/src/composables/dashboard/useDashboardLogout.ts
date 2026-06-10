import { useRouter } from "vue-router";

import { redirectToLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

export function useDashboardLogout() {
    const router = useRouter();
    const authStore = useAuthStore();

    async function logout(): Promise<void> {
        if (!authStore.isAuthenticated) {
            return;
        }

        await redirectToLogout(router);
    }

    return {
        logout,
    };
}
