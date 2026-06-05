<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { ErrorPageQuickLink } from "@/pages/errors/error-pages.data";

defineProps<{
    links: ErrorPageQuickLink[];
}>();
</script>

<template>
    <section class="error-quick-links" aria-labelledby="error-quick-links-title">
        <h2 id="error-quick-links-title" class="error-section-title">
            <i class="fa-solid fa-rocket"></i>
            <span>Популярные разделы</span>
        </h2>

        <div class="error-quick-links__grid">
            <RouterLink
                v-for="link in links"
                :key="link.title"
                class="error-quick-link"
                :to="link.to"
            >
                <span class="error-quick-link__icon">
                    <i :class="link.icon"></i>
                </span>
                <span class="error-quick-link__content">
                    <strong>{{ link.title }}</strong>
                    <span>{{ link.description }}</span>
                </span>
            </RouterLink>
        </div>
    </section>
</template>
