<script setup lang="ts">
import DashboardCourseCard from "@/components/dashboard/cards/DashboardCourseCard.vue";
import DashboardEmptyState from "@/components/dashboard/shared/DashboardEmptyState.vue";
import DashboardSectionHead from "@/components/dashboard/shared/DashboardSectionHead.vue";
import type { DashboardCourseCardContent } from "@/components/dashboard/types/dashboard.types";

interface SectionContent {
    badge?: string;
    icon?: string;
    title: string;
    text?: string;
    emptyIcon?: string;
    emptyText?: string;
}

interface Props {
    content: SectionContent;
    courses: DashboardCourseCardContent[];
    emptyTitle: string;
    filters?: readonly string[];
    sectionClass?: string;
}

withDefaults(defineProps<Props>(), {
    filters: () => [],
    sectionClass: "",
});
</script>

<template>
    <section
        class="fade-in visible"
        :class="sectionClass"
    >
        <DashboardSectionHead
            :badge="content.badge"
            :icon="content.icon"
            :title="content.title"
            :text="content.text"
        >
            <template
                v-if="filters.length"
                #actions
            >
                <div class="dashboard-inline-actions">
                    <button
                        v-for="(filter, index) in filters"
                        :key="filter"
                        class="dashboard-filter-chip"
                        :class="{ 'is-active': index === 0 }"
                        type="button"
                    >
                        {{ filter }}
                    </button>
                </div>
            </template>
        </DashboardSectionHead>

        <div
            v-if="courses.length"
            class="dashboard-courses-grid"
        >
            <DashboardCourseCard
                v-for="course in courses"
                :key="course.id"
                :course="course"
            />
        </div>

        <DashboardEmptyState
            v-else
            :icon="content.emptyIcon"
            :title="emptyTitle"
            :text="content.emptyText || ''"
        />
    </section>
</template>
