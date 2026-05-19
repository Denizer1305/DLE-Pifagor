<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";

interface Props {
    isDarkTheme: boolean;
}

interface Emits {
    (event: "toggle"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
const { t } = useI18n();
</script>

<template>
    <button
        class="theme-toggle"
        type="button"
        :aria-label="t('common.switchTheme')"
        @click="emit('toggle')"
    >
        <i class="base-icon fa-solid fa-sun"></i>
        <i class="base-icon fa-solid fa-moon"></i>
    </button>
</template>
