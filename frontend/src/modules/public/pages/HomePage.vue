<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import PublicLayout from "@/layouts/PublicLayout.vue";
import HomeAiSection from "@/modules/public/components/home/HomeAiSection.vue";
import HomeCtaSection from "@/modules/public/components/home/HomeCtaSection.vue";
import HomeFeaturesSection from "@/modules/public/components/home/HomeFeaturesSection.vue";
import HomeHeroSection from "@/modules/public/components/home/HomeHeroSection.vue";
import HomePartnersSection from "@/modules/public/components/home/HomePartnersSection.vue";
import HomeTestimonialsSection from "@/modules/public/components/home/HomeTestimonialsSection.vue";
import { homePageContent } from "@/modules/public/data/home-page.data";

const { localizePublicContent } = useI18n();

const content = computed(() => {
    return localizePublicContent(homePageContent);
});
</script>

<template>
    <PublicLayout>
        <HomeHeroSection :content="content.hero" />
        <HomeFeaturesSection :content="content.features" />
        <HomeAiSection :content="content.ai" />
        <HomePartnersSection :content="content.partners" />
        <HomeTestimonialsSection :content="content.testimonials" />
        <HomeCtaSection :content="content.cta" />
    </PublicLayout>
</template>
