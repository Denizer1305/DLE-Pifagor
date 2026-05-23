<script setup lang="ts">
interface Props {
    icon?: string;
    title?: string;
    text: string;
}

defineProps<Props>();
</script>

<template>
    <div class="dashboard-empty-state">
        <i
            v-if="icon"
            :class="icon"
        ></i>

        <strong v-if="title">
            {{ title }}
        </strong>

        <span>{{ text }}</span>
    </div>
</template>