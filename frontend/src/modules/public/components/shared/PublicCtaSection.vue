<script setup lang="ts">
import { RouterLink } from "vue-router";

import { useI18n } from "@/composables/useI18n";
import type { PublicCtaAction } from "@/modules/public/types/public.types";

interface Props {
    eyebrow?: string;
    title: string;
    description: string;
    actions: PublicCtaAction[];
}

const props = defineProps<Props>();
const { t } = useI18n();
</script>

<template>
    <section class="public-cta-section">
        <div class="container">
            <div class="public-cta-section__card">
                <p class="public-cta-section__eyebrow">
                    {{ props.eyebrow || t("common.getStarted") }}
                </p>

                <h2 class="public-cta-section__title">
                    {{ title }}
                </h2>

                <p class="public-cta-section__description">
                    {{ description }}
                </p>

                <div class="public-cta-section__actions">
                    <RouterLink
                        v-for="action in actions"
                        :key="action.routeName"
                        :to="{ name: action.routeName }"
                        :class="[
                            'public-cta-section__button',
                            `public-cta-section__button--${action.variant}`,
                        ]"
                    >
                        {{ action.label }}
                    </RouterLink>
                </div>
            </div>
        </div>
    </section>
</template>
