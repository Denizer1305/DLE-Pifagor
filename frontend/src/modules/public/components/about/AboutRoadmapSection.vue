<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import AboutRoadmapStep from "@/modules/public/components/about/AboutRoadmapStep.vue";
import type { AboutRoadmapContent } from "@/modules/public/data/about-page.data";

interface Props {
    content: AboutRoadmapContent;
}

defineProps<Props>();
</script>

<template>
    <section class="section about-roadmap">
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <p class="about-roadmap-intro fade-in">
                {{ content.intro }}
            </p>

            <div class="about-roadmap-track">
                <AboutRoadmapStep
                    v-for="stepItem in content.steps"
                    :key="stepItem.title"
                    :step="stepItem"
                />
            </div>
        </div>
    </section>
</template>
