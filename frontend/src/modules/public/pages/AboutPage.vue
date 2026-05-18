<script setup lang="ts">
import PublicLayout from "@/layouts/PublicLayout.vue";
import AboutCtaSection from "@/modules/public/components/about/AboutCtaSection.vue";
import AboutGratitudeSection from "@/modules/public/components/about/AboutGratitudeSection.vue";
import AboutHeroSection from "@/modules/public/components/about/AboutHeroSection.vue";
import AboutMissionSection from "@/modules/public/components/about/AboutMissionSection.vue";
import AboutRoadmapSection from "@/modules/public/components/about/AboutRoadmapSection.vue";
import AboutStorySection from "@/modules/public/components/about/AboutStorySection.vue";
import AboutTeamSection from "@/modules/public/components/about/AboutTeamSection.vue";
import { aboutPageContent } from "@/modules/public/data/about-page.data";
</script>

<template>
    <PublicLayout>
        <AboutHeroSection :content="aboutPageContent.hero" />
        <AboutStorySection :content="aboutPageContent.story" />
        <AboutMissionSection :content="aboutPageContent.mission" />
        <AboutRoadmapSection :content="aboutPageContent.roadmap" />
        <AboutTeamSection :content="aboutPageContent.team" />
        <AboutGratitudeSection :content="aboutPageContent.gratitude" />
        <AboutCtaSection :content="aboutPageContent.cta" />
    </PublicLayout>
</template>
