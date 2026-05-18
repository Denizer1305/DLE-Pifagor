<script setup lang="ts">
interface Props {
    icon: string;
    label: string;
}

defineProps<Props>();
</script>

<template>
    <span class="public-badge">
        <i :class="icon"></i>
        {{ label }}
    </span>
</template>
