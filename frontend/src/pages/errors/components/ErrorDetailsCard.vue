<script setup lang="ts">
import type { ErrorPageDetails } from "@/pages/errors/error-pages.data";

defineProps<{
    details: ErrorPageDetails;
}>();
</script>

<template>
    <article class="error-details-card">
        <h2 class="error-details-card__title">
            <i :class="details.icon"></i>
            <span>{{ details.title }}</span>
        </h2>

        <ul class="error-details-card__list">
            <li
                v-for="item in details.items"
                :key="item"
            >
                {{ item }}
            </li>
        </ul>
    </article>
</template>
