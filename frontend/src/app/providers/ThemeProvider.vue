<script setup lang="ts">
import { onMounted } from "vue";

import { useThemeStore } from "@/stores/theme.store";

const themeStore = useThemeStore();

onMounted(() => {
    themeStore.initTheme();
});
</script>

<template>
    <slot />
</template>
