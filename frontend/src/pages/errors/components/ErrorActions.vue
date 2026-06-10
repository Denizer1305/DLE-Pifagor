<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { ErrorPageAction } from "@/pages/errors/error-pages.data";

defineProps<{
    actions: ErrorPageAction[];
}>();

const emit = defineEmits<{
    (event: "action", action: ErrorPageAction): void;
}>();

function getActionClass(action: ErrorPageAction): string[] {
    return [
        "error-action",
        `error-action--${action.variant || "secondary"}`,
    ];
}
</script>

<template>
    <div class="error-actions">
        <template
            v-for="action in actions"
            :key="action.label"
        >
            <RouterLink
                v-if="action.to"
                :class="getActionClass(action)"
                :to="action.to"
            >
                <i :class="action.icon"></i>
                <span>{{ action.label }}</span>
            </RouterLink>

            <button
                v-else
                :class="getActionClass(action)"
                type="button"
                @click="emit('action', action)"
            >
                <i :class="action.icon"></i>
                <span>{{ action.label }}</span>
            </button>
        </template>
    </div>
</template>
