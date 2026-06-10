<script setup lang="ts">
import ErrorPageView from "@/pages/errors/ErrorPageView.vue";

import { forbiddenPageContent } from "./error-pages.data";
</script>

<template>
    <ErrorPageView :content="forbiddenPageContent" />
</template>
