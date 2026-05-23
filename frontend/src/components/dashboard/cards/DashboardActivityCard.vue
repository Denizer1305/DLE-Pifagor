<script setup lang="ts">
import { RouterLink } from "vue-router";

import DashboardEmptyState from "@/components/dashboard/shared/DashboardEmptyState.vue";
import DashboardSectionHead from "@/components/dashboard/shared/DashboardSectionHead.vue";
import type { DashboardCardSectionContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardCardSectionContent;
    cardClass?: string;
    emptyIcon?: string;
    emptyTitle?: string;
}

withDefaults(defineProps<Props>(), {
    cardClass: "",
    emptyIcon: "",
    emptyTitle: "",
});
</script>

<template>
    <section
        class="dashboard-card dashboard-activity-card fade-in visible"
        :class="cardClass"
    >
        <div class="dashboard-card-inner">
            <DashboardSectionHead
                :badge="content.badge"
                :icon="content.icon"
                :title="content.title"
                :text="content.text"
            >
                <template #actions>
                    <RouterLink
                        v-if="content.action?.to"
                        class="dashboard-card-action"
                        :to="content.action.to"
                    >
                        <i
                            v-if="content.action.icon"
                            :class="content.action.icon"
                        ></i>
                        {{ content.action.label }}
                    </RouterLink>

                    <a
                        v-else-if="content.action"
                        class="dashboard-card-action"
                        :href="content.action.href || '#'"
                    >
                        <i
                            v-if="content.action.icon"
                            :class="content.action.icon"
                        ></i>
                        {{ content.action.label }}
                    </a>
                </template>
            </DashboardSectionHead>

            <div
                v-if="content.items.length"
                class="dashboard-activity-list"
            >
                <article
                    v-for="item in content.items"
                    :key="item.id"
                    class="dashboard-activity-item"
                    :class="item.tone ? `is-${item.tone}` : ''"
                >
                    <div class="dashboard-activity-icon">
                        <i :class="item.icon"></i>
                    </div>

                    <div class="dashboard-activity-copy">
                        <strong>{{ item.title }}</strong>
                        <span>{{ item.text }}</span>
                        <small v-if="item.meta">{{ item.meta }}</small>
                    </div>
                </article>
            </div>

            <DashboardEmptyState
                v-else
                :icon="emptyIcon"
                :title="emptyTitle"
                :text="content.emptyText || ''"
            />
        </div>
    </section>
</template>
