<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardAiCardContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardAiCardContent;
}

defineProps<Props>();
</script>

<template>
    <section class="dashboard-card dashboard-ai-card fade-in visible">
        <div class="dashboard-card-inner">
            <div class="dashboard-ai-top">
                <div class="dashboard-ai-logo">
                    <img
                        :src="content.image.src"
                        :alt="content.image.alt"
                    />
                </div>

                <div>
                    <div class="dashboard-ai-title">
                        {{ content.title }}
                    </div>

                    <div class="dashboard-ai-subtitle">
                        {{ content.subtitle }}
                    </div>
                </div>
            </div>

            <div class="dashboard-ai-prompt">
                {{ content.text }}
            </div>

            <div class="dashboard-ai-actions">
                <template
                    v-for="action in content.actions || [content.action]"
                    :key="action.label"
                >
                    <RouterLink
                        v-if="action.to"
                        class="dashboard-ai-action"
                        :to="action.to"
                    >
                        <i
                            v-if="action.icon"
                            :class="action.icon"
                        ></i>
                        {{ action.label }}
                    </RouterLink>

                    <a
                        v-else
                        class="dashboard-ai-action"
                        :href="action.href || '#'"
                    >
                        <i
                            v-if="action.icon"
                            :class="action.icon"
                        ></i>
                        {{ action.label }}
                    </a>
                </template>
            </div>
        </div>
    </section>
</template>
