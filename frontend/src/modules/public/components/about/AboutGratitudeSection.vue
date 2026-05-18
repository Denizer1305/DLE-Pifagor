<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import AboutGratitudeCard from "@/modules/public/components/about/AboutGratitudeCard.vue";
import type { AboutGratitudeContent } from "@/modules/public/data/about-page.data";

interface Props {
    content: AboutGratitudeContent;
}

defineProps<Props>();
</script>

<template>
    <section
        id="gratitude"
        class="section gratitude-section"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.subtitle"
            />

            <div class="gratitude-architecture">
                <div class="gratitude-column">
                    <AboutGratitudeCard
                        v-for="card in content.leftCards"
                        :key="card.title"
                        :card="card"
                    />
                </div>

                <article class="gratitude-center fade-in">
                    <div class="gratitude-center-inner">
                        <div class="gratitude-center-mark">
                            <i :class="content.center.icon"></i>
                        </div>

                        <h3 class="gratitude-center-title">
                            {{ content.center.title }}
                        </h3>

                        <p class="gratitude-center-text">
                            {{ content.center.text }}
                        </p>

                        <div class="gratitude-center-note">
                            {{ content.center.note }}
                        </div>
                    </div>
                </article>

                <div class="gratitude-column">
                    <AboutGratitudeCard
                        v-for="card in content.rightCards"
                        :key="card.title"
                        :card="card"
                    />
                </div>
            </div>
        </div>
    </section>
</template>
