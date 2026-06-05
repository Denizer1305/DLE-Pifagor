<script setup lang="ts">
import { RouterLink } from "vue-router";

import NotificationEmptyState from "@/modules/notifications/components/NotificationEmptyState.vue";
import NotificationItem from "@/modules/notifications/components/NotificationItem.vue";
import type { NotificationViewModel } from "@/modules/notifications/types/notifications.types";

interface Props {
    items: NotificationViewModel[];
    unreadCount: number;
    isOpen: boolean;
    isLoading?: boolean;
    disabled?: boolean;
}

interface Emits {
    (event: "close"): void;
    (event: "read", id: number): void;
    (event: "read-all"): void;
    (event: "complete", id: number): void;
    (event: "remove", id: number): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div
        v-if="isOpen"
        class="notification-dropdown"
    >
        <div class="notification-dropdown__head">
            <div>
                <strong>Уведомления</strong>
                <span>{{ unreadCount }} непрочитанных</span>
            </div>

            <button
                type="button"
                class="notification-dropdown__close"
                @click="emit('close')"
            >
                <i class="fas fa-xmark"></i>
            </button>
        </div>

        <div class="notification-dropdown__actions">
            <button
                type="button"
                :disabled="disabled || unreadCount === 0"
                @click="emit('read-all')"
            >
                <i class="fas fa-check-double"></i>
                Прочитать все
            </button>

            <RouterLink
                :to="{ name: 'notifications' }"
                @click="emit('close')"
            >
                Открыть центр
            </RouterLink>
        </div>

        <div class="notification-dropdown__body">
            <div
                v-if="isLoading"
                class="notification-dropdown__loading"
            >
                <i class="fas fa-spinner"></i>
                <span>Загружаем...</span>
            </div>

            <NotificationEmptyState
                v-else-if="!items.length"
                title="Нет новых уведомлений"
                text="Все важные события уже обработаны."
            />

            <NotificationItem
                v-for="item in items"
                v-else
                :key="item.id"
                :notification="item"
                :disabled="disabled"
                compact
                @read="emit('read', $event)"
                @complete="emit('complete', $event)"
                @remove="emit('remove', $event)"
            />
        </div>
    </div>
</template>