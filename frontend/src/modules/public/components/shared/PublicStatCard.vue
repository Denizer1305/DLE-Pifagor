<script setup lang="ts">
interface Props {
    value: string;
    label: string;
    description?: string;
}

withDefaults(defineProps<Props>(), {
    description: "",
});
</script>

<template>
    <article class="public-stat-card">
        <strong class="public-stat-card__value">
            {{ value }}
        </strong>

        <span class="public-stat-card__label">
            {{ label }}
        </span>

        <p
            v-if="description"
            class="public-stat-card__description"
        >
            {{ description }}
        </p>
    </article>
</template>
