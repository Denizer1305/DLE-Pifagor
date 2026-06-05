<script setup lang="ts">
import type {
    NotificationFilterOption,
    NotificationStatus,
} from "@/modules/notifications/types/notifications.types";

interface Props {
    modelValue: NotificationStatus | "";
    options: NotificationFilterOption[];
    disabled?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: NotificationStatus | ""): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div class="notification-status-tabs">
        <button
            v-for="option in options"
            :key="option.value"
            type="button"
            class="notification-status-tabs__item"
            :class="{ 'is-active': option.value === modelValue }"
            :disabled="disabled"
            @click="emit('update:modelValue', option.value as NotificationStatus | '')"
        >
            <i
                v-if="option.icon"
                :class="option.icon"
            ></i>
            {{ option.label }}
        </button>
    </div>
</template>