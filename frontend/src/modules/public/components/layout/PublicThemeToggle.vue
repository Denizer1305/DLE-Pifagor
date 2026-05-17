<script setup lang="ts">
import { computed } from "vue";

interface Props {
    isDarkTheme: boolean;
}

interface Emits {
    (event: "toggle"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const iconClass = computed(() => {
    return props.isDarkTheme
        ? "fa-solid fa-sun"
        : "fa-solid fa-moon";
});

const label = computed(() => {
    return props.isDarkTheme
        ? "Включить светлую тему"
        : "Включить тёмную тему";
});
</script>

<template>
    <button
        class="public-theme-toggle"
        type="button"
        :aria-label="label"
        @click="emit('toggle')"
    >
        <i :class="iconClass"></i>
    </button>
</template>