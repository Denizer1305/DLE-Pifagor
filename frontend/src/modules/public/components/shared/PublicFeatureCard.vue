<script setup lang="ts">
interface Props {
    icon: string;
    title: string;
    description: string;
}

defineProps<Props>();
</script>

<template>
    <article class="public-feature-card">
        <div class="public-feature-card__icon">
            <i :class="icon"></i>
        </div>

        <h3 class="public-feature-card__title">
            {{ title }}
        </h3>

        <p class="public-feature-card__description">
            {{ description }}
        </p>
    </article>
</template>
