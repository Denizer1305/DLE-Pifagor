<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import HomeFeatureCard from "@/modules/public/components/home/HomeFeatureCard.vue";
import type { HomeFeaturesContent } from "@/modules/public/data/home-page.data";

interface Props {
    content: HomeFeaturesContent;
}

defineProps<Props>();
</script>

<template>
    <section
        id="features"
        class="section features"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="features-layout">
                <div class="features-col main">
                    <HomeFeatureCard
                        v-for="card in content.mainCards"
                        :key="card.variant || card.icon"
                        :card="card"
                    />
                </div>

                <div class="features-col side">
                    <HomeFeatureCard
                        v-for="card in content.sideCards"
                        :key="card.variant || card.icon"
                        :card="card"
                    />
                </div>
            </div>
        </div>
    </section>
</template>
