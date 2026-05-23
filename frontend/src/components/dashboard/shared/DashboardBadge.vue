<script setup lang="ts">
interface Props {
    icon?: string;
    label: string;
}

defineProps<Props>();
</script>

<template>
    <span class="dashboard-badge">
        <i
            v-if="icon"
            :class="icon"
        ></i>
        {{ label }}
    </span>
</template>
