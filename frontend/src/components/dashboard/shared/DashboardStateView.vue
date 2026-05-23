<script setup lang="ts">
type DashboardStateViewVariant = "loading" | "error" | "empty";

interface Props {
    variant: DashboardStateViewVariant;
    title?: string;
    text: string;
    actionLabel?: string;
    actionIcon?: string;
}

interface Emits {
    (event: "action"): void;
}

defineProps<Props>();
defineEmits<Emits>();

function getIcon(variant: DashboardStateViewVariant): string {
    const icons: Record<DashboardStateViewVariant, string> = {
        loading: "fas fa-spinner",
        error: "fas fa-triangle-exclamation",
        empty: "fas fa-circle-info",
    };

    return icons[variant];
}
</script>

<template>
    <div
        class="dashboard-state-view"
        :class="`is-${variant}`"
    >
        <div class="dashboard-state-view__icon">
            <i :class="getIcon(variant)"></i>
        </div>

        <div class="dashboard-state-view__content">
            <strong v-if="title">
                {{ title }}
            </strong>

            <p>
                {{ text }}
            </p>
        </div>

        <button
            v-if="actionLabel"
            type="button"
            class="dashboard-quick-btn primary"
            @click="$emit('action')"
        >
            <i
                v-if="actionIcon"
                :class="actionIcon"
            ></i>

            {{ actionLabel }}
        </button>
    </div>
</template>