<script setup lang="ts">
import ThemeProvider from "@/app/providers/ThemeProvider.vue";
</script>

<template>
    <ThemeProvider>
        <slot />
    </ThemeProvider>
</template>
