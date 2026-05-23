<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";

interface Props {
    icon: string;
    topline: string;
    title: string;
    description: string;
}

defineProps<Props>();
const { tr } = useI18n();
</script>

<template>
    <div class="auth-form-topline">
        <i :class="icon"></i>
        {{ tr(topline) }}
    </div>

    <h2 class="auth-form-title">
        {{ tr(title) }}
    </h2>

    <p class="auth-form-description">
        {{ tr(description) }}
    </p>

    <slot />
</template>
