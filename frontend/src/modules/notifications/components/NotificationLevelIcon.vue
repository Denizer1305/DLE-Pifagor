<script setup lang="ts">
import type { NotificationLevel } from "@/modules/notifications/types/notifications.types";

interface Props {
    level: NotificationLevel;
    icon: string;
}

defineProps<Props>();
</script>

<template>
    <span
        class="notification-level-icon"
        :class="`is-${level}`"
    >
        <i :class="icon"></i>
    </span>
</template>
