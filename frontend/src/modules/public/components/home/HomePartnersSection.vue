<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import HomePartnerCard from "@/modules/public/components/home/HomePartnerCard.vue";

interface Props {
    content: {
        label: string;
        title: string;
        description: string;
        intro: {
            label: string;
            title: string;
            text: string;
        };
        accent: {
            icon: string;
            title: string;
            text: string;
        };
        items: {
            variant?: string;
            tag: string;
            name: string;
            text: string;
            image: {
                src: string;
                alt: string;
            };
        }[];
    };
}

defineProps<Props>();
const { t } = useI18n();
</script>

<template>
    <section
        id="partners"
        class="section partners-section"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="partners-shell fade-in">
                <div class="partners-intro">
                    <article class="partners-intro-card">
                        <div class="partners-kicker">
                            {{ content.intro.label }}
                        </div>

                        <h3>
                            {{ content.intro.title }}
                        </h3>

                        <p>
                            {{ content.intro.text }}
                        </p>
                    </article>
                </div>

                <div
                    class="partners-diptych"
                    :aria-label="t('common.platformPartners')"
                >
                    <HomePartnerCard
                        v-if="content.items[0]"
                        :partner="content.items[0]"
                    />

                    <div
                        class="partners-accent"
                        aria-hidden="true"
                    >
                        <div class="partners-accent-mark">
                            <i :class="content.accent.icon"></i>
                        </div>

                        <h4>
                            {{ content.accent.title }}
                        </h4>

                        <p>
                            {{ content.accent.text }}
                        </p>
                    </div>

                    <HomePartnerCard
                        v-if="content.items[1]"
                        :partner="content.items[1]"
                    />
                </div>

                <div class="partners-grid mobile-only">
                    <HomePartnerCard
                        v-for="partner in content.items"
                        :key="partner.name"
                        :partner="partner"
                        mode="card"
                    />
                </div>
            </div>
        </div>
    </section>
</template>
