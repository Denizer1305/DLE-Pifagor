<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import PublicLayout from "@/layouts/PublicLayout.vue";
import AboutCtaSection from "@/modules/public/components/about/AboutCtaSection.vue";
import AboutGratitudeSection from "@/modules/public/components/about/AboutGratitudeSection.vue";
import AboutHeroSection from "@/modules/public/components/about/AboutHeroSection.vue";
import AboutMissionSection from "@/modules/public/components/about/AboutMissionSection.vue";
import AboutRoadmapSection from "@/modules/public/components/about/AboutRoadmapSection.vue";
import AboutStorySection from "@/modules/public/components/about/AboutStorySection.vue";
import AboutTeamSection from "@/modules/public/components/about/AboutTeamSection.vue";
import { aboutPageContent } from "@/modules/public/data/about-page.data";

const { localizePublicContent } = useI18n();

const content = computed(() => {
    return localizePublicContent(aboutPageContent);
});
</script>

<template>
    <PublicLayout>
        <AboutHeroSection :content="content.hero" />
        <AboutStorySection :content="content.story" />
        <AboutMissionSection :content="content.mission" />
        <AboutRoadmapSection :content="content.roadmap" />
        <AboutTeamSection :content="content.team" />
        <AboutGratitudeSection :content="content.gratitude" />
        <AboutCtaSection :content="content.cta" />
    </PublicLayout>
</template>
