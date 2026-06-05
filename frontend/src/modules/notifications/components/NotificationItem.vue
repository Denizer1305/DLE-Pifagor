<script setup lang="ts">
import { RouterLink } from "vue-router";

import NotificationLevelIcon from "@/modules/notifications/components/NotificationLevelIcon.vue";
import type { NotificationViewModel } from "@/modules/notifications/types/notifications.types";
import { getNotificationActionTarget } from "@/modules/notifications/mappers/notification.mapper";

interface Props {
    notification: NotificationViewModel;
    compact?: boolean;
    disabled?: boolean;
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
    <article
        class="notification-item"
        :class="[
            `is-${notification.level}`,
            {
                'is-unread': notification.isUnread,
                'is-compact': compact,
            },
        ]"
    >
        <NotificationLevelIcon
            :level="notification.level"
            :icon="notification.levelIcon"
        />

        <div class="notification-item__body">
            <div class="notification-item__head">
                <div>
                    <h3>{{ notification.title }}</h3>

                    <div class="notification-item__meta">
                        <span>{{ notification.categoryLabel }}</span>
                        <span>{{ notification.createdAtLabel }}</span>
                        <span v-if="notification.eventAtLabel">
                            Событие: {{ notification.eventAtLabel }}
                        </span>
                    </div>
                </div>

                <span
                    v-if="notification.isUnread"
                    class="notification-item__status"
                >
                    Новое
                </span>
            </div>

            <p class="notification-item__message">
                {{ notification.message }}
            </p>

            <div class="notification-item__footer">
                <RouterLink
                    v-if="notification.hasAction"
                    class="notification-item__action"
                    :to="getNotificationActionTarget(notification.actionUrl)"
                >
                    {{ notification.actionLabel || "Открыть" }}
                    <i class="fas fa-arrow-right"></i>
                </RouterLink>

                <div class="notification-item__buttons">
                    <button
                        v-if="notification.isUnread"
                        type="button"
                        :disabled="disabled"
                        @click="emit('read', notification.id)"
                    >
                        <i class="fas fa-envelope-open"></i>
                        Прочитать
                    </button>

                    <button
                        v-if="notification.status !== 'completed'"
                        type="button"
                        :disabled="disabled"
                        @click="emit('complete', notification.id)"
                    >
                        <i class="fas fa-circle-check"></i>
                        Выполнено
                    </button>

                    <button
                        type="button"
                        class="is-danger"
                        :disabled="disabled"
                        @click="emit('remove', notification.id)"
                    >
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    </article>
</template>