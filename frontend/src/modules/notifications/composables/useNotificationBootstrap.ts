import { computed } from "vue";

import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";
import type { NotificationBootstrapPayload } from "@/modules/notifications/types/notifications.types";

export function useNotificationBootstrap() {
    const notificationsStore = useNotificationsStore();

    const isBootstrapping = computed(() => notificationsStore.isBootstrapping);
    const lastBootstrapDate = computed(() => notificationsStore.lastBootstrapDate);
    const errorMessage = computed(() => notificationsStore.errorMessage);

    async function bootstrap(
        payload: NotificationBootstrapPayload = {
            reason: "dashboard_login",
        },
    ): Promise<void> {
        await notificationsStore.bootstrap(payload);
    }

    return {
        isBootstrapping,
        lastBootstrapDate,
        errorMessage,
        bootstrap,
    };
}