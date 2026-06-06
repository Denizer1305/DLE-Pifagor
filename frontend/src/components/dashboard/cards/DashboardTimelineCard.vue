<script setup lang="ts">
import { RouterLink } from "vue-router";

import DashboardEmptyState from "@/components/dashboard/shared/DashboardEmptyState.vue";
import DashboardSectionHead from "@/components/dashboard/shared/DashboardSectionHead.vue";
import type {
    DashboardAction,
    DashboardTimelineContent,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardTimelineContent;
    cardClass?: string;
    emptyIcon?: string;
    emptyTitle?: string;
}

withDefaults(defineProps<Props>(), {
    cardClass: "",
    emptyIcon: "",
    emptyTitle: "",
});

const emit = defineEmits<{
    (event: "create", kind: "calendar" | "note"): void;
}>();

function handleAction(action: DashboardAction): void {
    if (action.createKind) {
        emit("create", action.createKind);
    }
}
</script>

<template>
    <section
        class="dashboard-card dashboard-timeline-card fade-in visible"
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
                    <div class="dashboard-inline-actions">
                        <button
                            v-for="action in content.actions?.filter((item) => item.createKind)"
                            :key="`${action.createKind}-${action.label}`"
                            type="button"
                            class="dashboard-card-action"
                            :class="action.variant ? `is-${action.variant}` : ''"
                            @click="handleAction(action)"
                        >
                            <i
                                v-if="action.icon"
                                :class="action.icon"
                            ></i>
                            {{ action.label }}
                        </button>

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
                    </div>
                </template>
            </DashboardSectionHead>

            <div
                v-if="content.items.length"
                class="dashboard-timeline"
            >
                <article
                    v-for="item in content.items"
                    :key="item.id"
                    class="dashboard-timeline-item"
                    :class="item.tone ? `is-${item.tone}` : ''"
                >
                    <div class="dashboard-timeline-time">
                        {{ item.time }}
                    </div>

                    <div class="dashboard-timeline-line">
                        <span class="dashboard-timeline-dot"></span>
                    </div>

                    <div class="dashboard-timeline-card">
                        <strong>{{ item.title }}</strong>
                        <span>{{ item.text }}</span>
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
