<script setup lang="ts">
import { RouterLink } from "vue-router";

import type {
    DashboardAction,
    DashboardCourseCardContent,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    course: DashboardCourseCardContent;
}

defineProps<Props>();

function getStatusClass(statusVariant?: string): string[] {
    return [
        "dashboard-course-status",
        statusVariant || "",
    ].filter(Boolean);
}

function getActionClass(action: DashboardAction): string[] {
    return [
        "dashboard-course-btn",
        action.variant === "primary" ? "primary" : "",
    ].filter(Boolean);
}

function getProgressValue(value?: number): number {
    if (typeof value !== "number") {
        return 0;
    }

    return Math.min(100, Math.max(0, value));
}
</script>

<template>
    <article class="dashboard-course-card fade-in visible">
        <div class="dashboard-course-top">
            <div class="dashboard-course-mark">
                <i :class="course.icon"></i>
            </div>

            <div :class="getStatusClass(course.statusVariant)">
                {{ course.status }}
            </div>
        </div>

        <h3 class="dashboard-course-title">
            {{ course.title }}
        </h3>

        <p class="dashboard-course-desc">
            {{ course.description }}
        </p>

        <div
            v-if="course.meta.length"
            class="dashboard-course-meta"
        >
            <div
                v-for="item in course.meta"
                :key="item.label"
                class="dashboard-course-meta-item"
            >
                <strong>{{ item.value }}</strong>
                <span>{{ item.label }}</span>
            </div>
        </div>

        <div
            v-if="course.progress !== undefined"
            class="dashboard-course-progress"
        >
            <div class="dashboard-progress-head">
                <span class="dashboard-progress-label">{{ course.progressLabel || "" }}</span>
                <span class="dashboard-progress-label">{{ getProgressValue(course.progress) }}%</span>
            </div>

            <div class="dashboard-progress-track">
                <div
                    class="dashboard-progress-bar"
                    :style="{ width: `${getProgressValue(course.progress)}%` }"
                ></div>
            </div>
        </div>

        <div
            v-if="course.actions?.length"
            class="dashboard-course-actions"
        >
            <template
                v-for="action in course.actions"
                :key="action.label"
            >
                <RouterLink
                    v-if="action.to"
                    :class="getActionClass(action)"
                    :to="action.to"
                >
                    {{ action.label }}
                </RouterLink>

                <a
                    v-else
                    :class="getActionClass(action)"
                    :href="action.href || '#'"
                >
                    {{ action.label }}
                </a>
            </template>
        </div>
    </article>
</template>
