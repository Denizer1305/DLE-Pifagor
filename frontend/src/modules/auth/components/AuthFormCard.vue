<script setup lang="ts">
interface Props {
    icon: string;
    topline: string;
    title: string;
    description: string;
}

defineProps<Props>();
</script>

<template>
    <div class="auth-form-topline">
        <i :class="icon"></i>
        {{ topline }}
    </div>

    <h2 class="auth-form-title">
        {{ title }}
    </h2>

    <p class="auth-form-description">
        {{ description }}
    </p>

    <slot />
</template>
