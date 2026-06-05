<script setup lang="ts">
import ErrorPageView from "@/pages/errors/ErrorPageView.vue";

import { notFoundPageContent } from "./error-pages.data";
</script>

<template>
    <ErrorPageView :content="notFoundPageContent" />
</template>
