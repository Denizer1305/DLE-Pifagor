import { computed, onMounted } from "vue";

import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";

export function useNotificationUnreadCount() {
    const notificationsStore = useNotificationsStore();

    const unreadCount = computed(() => notificationsStore.unreadCount);
    const hasUnread = computed(() => notificationsStore.hasUnread);

    async function loadUnreadCount(): Promise<void> {
        await notificationsStore.loadUnreadCount();
    }

    onMounted(() => {
        void loadUnreadCount();
    });

    return {
        unreadCount,
        hasUnread,
        loadUnreadCount,
    };
}
