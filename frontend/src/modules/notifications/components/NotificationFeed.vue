<script setup lang="ts">
import NotificationEmptyState from "@/modules/notifications/components/NotificationEmptyState.vue";
import NotificationItem from "@/modules/notifications/components/NotificationItem.vue";
import type { NotificationViewModel } from "@/modules/notifications/types/notifications.types";

interface Props {
    items: NotificationViewModel[];
    isLoading?: boolean;
    disabled?: boolean;
    compact?: boolean;
}

interface Emits {
    (event: "read", id: number): void;
    (event: "complete", id: number): void;
    (event: "remove", id: number): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div class="notification-feed">
        <div
            v-if="isLoading"
            class="notification-feed__loading"
        >
            <i class="fas fa-spinner"></i>
            <span>Загружаем уведомления...</span>
        </div>

        <NotificationEmptyState
            v-else-if="!items.length"
        />

        <div
            v-else
            class="notification-feed__list"
        >
            <NotificationItem
                v-for="item in items"
                :key="item.id"
                :notification="item"
                :compact="compact"
                :disabled="disabled"
                @read="emit('read', $event)"
                @complete="emit('complete', $event)"
                @remove="emit('remove', $event)"
            />
        </div>
    </div>
</template>
