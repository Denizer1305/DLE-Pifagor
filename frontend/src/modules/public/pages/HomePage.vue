<script setup lang="ts">
import PublicLayout from "@/layouts/PublicLayout.vue";
import HomeAiSection from "@/modules/public/components/home/HomeAiSection.vue";
import HomeCtaSection from "@/modules/public/components/home/HomeCtaSection.vue";
import HomeFeaturesSection from "@/modules/public/components/home/HomeFeaturesSection.vue";
import HomeHeroSection from "@/modules/public/components/home/HomeHeroSection.vue";
import HomePartnersSection from "@/modules/public/components/home/HomePartnersSection.vue";
import HomeTestimonialsSection from "@/modules/public/components/home/HomeTestimonialsSection.vue";
import { homePageContent } from "@/modules/public/data/home-page.data";
</script>

<template>
    <PublicLayout>
        <HomeHeroSection :content="homePageContent.hero" />
        <HomeFeaturesSection :content="homePageContent.features" />
        <HomeAiSection :content="homePageContent.ai" />
        <HomePartnersSection :content="homePageContent.partners" />
        <HomeTestimonialsSection :content="homePageContent.testimonials" />
        <HomeCtaSection :content="homePageContent.cta" />
    </PublicLayout>
</template>
