<script setup lang="ts">
interface Props {
    name: string;
    icon: string;
    ariaLabel: string;
    buttonClass?: string;
    badge?: string | number;
    isOpen?: boolean;
}

interface Emits {
    (event: "toggle", name: string): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div class="dashboard-header-control">
        <button
            class="dashboard-icon-btn"
            :class="buttonClass"
            type="button"
            :data-dashboard-panel-toggle="name"
            :aria-label="ariaLabel"
            :aria-expanded="isOpen"
            @click="emit('toggle', name)"
        >
            <i :class="icon"></i>

            <span
                v-if="badge !== undefined && badge !== null"
                class="dashboard-icon-badge"
            >
                {{ badge }}
            </span>
        </button>

        <slot></slot>
    </div>
</template>
