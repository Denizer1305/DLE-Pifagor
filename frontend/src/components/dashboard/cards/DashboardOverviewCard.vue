<script setup lang="ts">
import DashboardEmptyState from "@/components/dashboard/shared/DashboardEmptyState.vue";
import DashboardSectionHead from "@/components/dashboard/shared/DashboardSectionHead.vue";

interface DashboardOverviewRow {
    id: string | number;
    cells: Array<string | number>;
    status: string;
    warning?: boolean;
}

interface Props {
    badge?: string;
    icon?: string;
    title: string;
    text?: string;
    headers: readonly string[];
    rows: DashboardOverviewRow[];
    emptyIcon?: string;
    emptyTitle?: string;
    emptyText?: string;
    cardClass?: string;
}

defineProps<Props>();
</script>

<template>
    <article
        class="dashboard-card fade-in visible"
        :class="cardClass"
    >
        <div class="dashboard-card-inner">
            <DashboardSectionHead
                :badge="badge"
                :icon="icon"
                :title="title"
                :text="text"
            />

            <div
                v-if="rows.length"
                class="dashboard-journal-table"
            >
                <div class="dashboard-journal-row head">
                    <span
                        v-for="header in headers"
                        :key="header"
                    >
                        {{ header }}
                    </span>
                </div>

                <div
                    v-for="row in rows"
                    :key="row.id"
                    class="dashboard-journal-row"
                >
                    <span
                        v-for="(cell, index) in row.cells"
                        :key="`${row.id}-${index}`"
                    >
                        {{ cell }}
                    </span>

                    <span
                        class="dashboard-journal-status"
                        :class="{ warn: row.warning }"
                    >
                        {{ row.status }}
                    </span>
                </div>
            </div>

            <DashboardEmptyState
                v-else
                :icon="emptyIcon"
                :title="emptyTitle"
                :text="emptyText || ''"
            />

            <slot name="actions"></slot>
        </div>
    </article>
</template>
