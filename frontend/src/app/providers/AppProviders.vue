<script setup lang="ts">
import AuthProvider from "@/app/providers/AuthProvider.vue";
import ThemeProvider from "@/app/providers/ThemeProvider.vue";
</script>

<template>
    <AuthProvider>
        <ThemeProvider>
            <slot />
        </ThemeProvider>
    </AuthProvider>
</template>
