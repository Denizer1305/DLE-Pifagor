<script setup lang="ts">
import { onMounted } from "vue";

import { useAuthStore } from "@/stores/auth.store";

const authStore = useAuthStore();

onMounted(() => {
    void authStore.initAuth().catch(() => undefined);
});
</script>

<template>
    <slot />
</template>
