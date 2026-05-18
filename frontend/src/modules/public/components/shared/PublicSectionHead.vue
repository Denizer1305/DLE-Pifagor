<script setup lang="ts">
interface Props {
    label?: string;
    title: string;
    description?: string;
}

withDefaults(defineProps<Props>(), {
    label: "",
    description: "",
});
</script>

<template>
    <div class="section-heading fade-in">
        <span
            v-if="label"
            class="section-label"
        >
            {{ label }}
        </span>

        <h2 class="section-title">
            {{ title }}
        </h2>

        <p
            v-if="description"
            class="section-description"
        >
            {{ description }}
        </p>
    </div>
</template>
