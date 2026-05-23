<script setup lang="ts">
interface Props {
    ariaLabel: string;
}

interface Emits {
    (event: "toggle"): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>

<template>
    <button
        class="dashboard-mobile-menu-btn"
        type="button"
        :aria-label="ariaLabel"
        @click="$emit('toggle')"
    >
        <i class="fas fa-bars"></i>
    </button>
</template>
