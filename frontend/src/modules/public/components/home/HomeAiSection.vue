<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import HomeAiCard from "@/modules/public/components/home/HomeAiCard.vue";
import HomeAiMiniCard from "@/modules/public/components/home/HomeAiMiniCard.vue";
import HomeAiOrbitCard from "@/modules/public/components/home/HomeAiOrbitCard.vue";

interface Props {
    content: {
        label: string;
        title: string;
        description: string;
        avatar: {
            src: string;
            alt: string;
        };
        cards: {
            variant?: string;
            label: string;
            icon: string;
            title: string;
            text: string;
            points?: string[];
            logic?: {
                title: string;
                text: string;
            }[];
            quote?: string;
            quoteSub?: string;
        }[];
        miniCards: {
            icon: string;
            title: string;
            text: string;
        }[];
    };
}

defineProps<Props>();

const backgroundCircles = ["one", "two", "three", "four"];
const backgroundLines = ["one", "two", "three"];
const backgroundGlows = ["one", "two"];
</script>

<template>
    <section
        id="anastasia-ai"
        class="section ai-section"
    >
        <div
            class="ai-bg"
            aria-hidden="true"
        >
            <div
                v-for="circle in backgroundCircles"
                :key="`ai-bg-circle-${circle}`"
                class="ai-bg-circle"
                :class="circle"
            ></div>

            <div
                v-for="line in backgroundLines"
                :key="`ai-bg-line-${line}`"
                class="ai-bg-line"
                :class="line"
            ></div>

            <div
                v-for="glow in backgroundGlows"
                :key="`ai-bg-glow-${glow}`"
                class="ai-bg-glow"
                :class="glow"
            ></div>
        </div>

        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="ai-layout">
                <HomeAiCard
                    v-if="content.cards[0]"
                    :card="content.cards[0]"
                />

                <HomeAiOrbitCard :avatar="content.avatar" />

                <HomeAiCard
                    v-if="content.cards[1]"
                    :card="content.cards[1]"
                />

                <HomeAiCard
                    v-if="content.cards[2]"
                    :card="content.cards[2]"
                />

                <div
                    v-if="content.miniCards.length"
                    class="ai-cards-stack fade-in"
                >
                    <HomeAiMiniCard
                        v-for="item in content.miniCards"
                        :key="item.title"
                        :item="item"
                    />
                </div>
            </div>
        </div>
    </section>
</template>
