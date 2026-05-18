<script setup lang="ts">
interface Props {
    isDarkTheme: boolean;
}

interface Emits {
    (event: "toggle"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <button
        class="theme-toggle"
        type="button"
        aria-label="Переключить тему"
        @click="emit('toggle')"
    >
        <i class="base-icon fa-solid fa-sun"></i>
        <i class="base-icon fa-solid fa-moon"></i>
    </button>
</template>
