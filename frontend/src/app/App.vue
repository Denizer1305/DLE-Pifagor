<script setup lang="ts">
import { RouterView } from "vue-router";

import AppProviders from "@/app/providers/AppProviders.vue";
import ToastContainer from "@/components/feedback/ToastContainer.vue";
</script>

<template>
    <AppProviders>
        <RouterView />
        <ToastContainer />
    </AppProviders>
</template>
