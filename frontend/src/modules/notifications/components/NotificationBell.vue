<script setup lang="ts">
import { computed, ref } from "vue";

import NotificationDropdown from "@/modules/notifications/components/NotificationDropdown.vue";
import NotificationUnreadBadge from "@/modules/notifications/components/NotificationUnreadBadge.vue";
import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";

const notificationsStore = useNotificationsStore();

const isOpen = ref(false);

const latestItems = computed(() => notificationsStore.latestItems);
const unreadCount = computed(() => notificationsStore.unreadCount);
const isLoading = computed(() => notificationsStore.isLoading);
const isActionLoading = computed(() => notificationsStore.isActionLoading);

function toggleDropdown(): void {
    isOpen.value = !isOpen.value;

    if (isOpen.value) {
        void notificationsStore.loadFeed();
    }
}

function closeDropdown(): void {
    isOpen.value = false;
}
</script>

<template>
    <div class="notification-bell">
        <button
            type="button"
            class="notification-bell__button"
            :class="{ 'has-unread': unreadCount > 0 }"
            aria-label="Открыть уведомления"
            @click="toggleDropdown"
        >
            <i class="fas fa-bell"></i>

            <NotificationUnreadBadge :count="unreadCount" />
        </button>

        <NotificationDropdown
            :items="latestItems"
            :unread-count="unreadCount"
            :is-open="isOpen"
            :is-loading="isLoading"
            :disabled="isActionLoading"
            @close="closeDropdown"
            @read="notificationsStore.markAsRead"
            @read-all="notificationsStore.markAllAsRead"
            @complete="notificationsStore.complete"
            @remove="notificationsStore.remove"
        />
    </div>
</template>
