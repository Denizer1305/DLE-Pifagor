<script setup lang="ts">
import { RouterView } from "vue-router";

import AppProviders from "@/app/providers/AppProviders.vue";
import ToastContainer from "@/components/feedback/ToastContainer.vue";

const appUi = {
    toastCloseLabel: "Закрыть уведомление",
};
</script>

<template>
    <AppProviders>
        <RouterView v-slot="{ Component, route }">
            <Transition
                name="page-fade"
                mode="out-in"
                appear
            >
                <component
                    :is="Component"
                    :key="route.fullPath"
                />
            </Transition>
        </RouterView>

        <ToastContainer :close-label="appUi.toastCloseLabel" />
    </AppProviders>
</template>
