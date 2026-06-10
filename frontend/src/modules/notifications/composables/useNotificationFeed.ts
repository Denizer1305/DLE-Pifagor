import { computed, onMounted, reactive } from "vue";

import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";
import type { NotificationQueryParams } from "@/modules/notifications/types/notifications.types";

export function useNotificationFeed() {
    const notificationsStore = useNotificationsStore();

    const filters = reactive<NotificationQueryParams>({
        status: "",
        level: "",
        category: "",
        notification_type: "",
        source_type: "",
        source_id: "",
        unread_only: false,
    });

    const items = computed(() => notificationsStore.items);
    const unreadCount = computed(() => notificationsStore.unreadCount);
    const isLoading = computed(() => notificationsStore.isLoading);
    const isActionLoading = computed(() => notificationsStore.isActionLoading);
    const errorMessage = computed(() => notificationsStore.errorMessage);

    async function loadFeed(): Promise<void> {
        await notificationsStore.loadFeed(filters);
    }

    async function updateFilter<K extends keyof NotificationQueryParams>(
        key: K,
        value: NotificationQueryParams[K],
    ): Promise<void> {
        filters[key] = value;
        await loadFeed();
    }

    async function clearFilters(): Promise<void> {
        filters.status = "";
        filters.level = "";
        filters.category = "";
        filters.notification_type = "";
        filters.source_type = "";
        filters.source_id = "";
        filters.unread_only = false;

        await loadFeed();
    }

    onMounted(() => {
        void loadFeed();
    });

    return {
        filters,
        items,
        unreadCount,
        isLoading,
        isActionLoading,
        errorMessage,
        loadFeed,
        updateFilter,
        clearFilters,
        markAsRead: notificationsStore.markAsRead,
        markAllAsRead: notificationsStore.markAllAsRead,
        complete: notificationsStore.complete,
        remove: notificationsStore.remove,
    };
}
