<script setup lang="ts">
interface Props {
    name?: string;
    panelClass?: string;
    isOpen?: boolean;
}

defineProps<Props>();
</script>

<template>
    <div
        class="dashboard-floating-panel"
        :class="[panelClass, { 'is-open': isOpen }]"
        :data-dashboard-panel="name"
    >
        <slot></slot>
    </div>
</template>
