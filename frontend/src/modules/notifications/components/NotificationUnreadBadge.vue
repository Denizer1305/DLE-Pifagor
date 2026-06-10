<script setup lang="ts">
interface Props {
    count: number;
    max?: number;
}

const props = withDefaults(defineProps<Props>(), {
    max: 99,
});
</script>

<template>
    <span
        v-if="count > 0"
        class="notification-unread-badge"
    >
        {{ count > props.max ? `${props.max}+` : count }}
    </span>
</template>
