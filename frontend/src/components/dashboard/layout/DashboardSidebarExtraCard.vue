<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardSidebarExtraCard } from "@/components/dashboard/types/dashboard.types";

interface Props {
    card: DashboardSidebarExtraCard;
}

const props = defineProps<Props>();

function getCardClass(): string {
    if (props.card.variant === "ai") {
        return "sidebar-ai";
    }

    if (props.card.variant === "student") {
        return "sidebar-student-card";
    }

    return "sidebar-extra-card";
}

function getTopClass(): string {
    if (props.card.variant === "ai") {
        return "sidebar-ai-top";
    }

    if (props.card.variant === "student") {
        return "sidebar-student-card-top";
    }

    return "sidebar-extra-card-top";
}

function getIconClass(): string {
    if (props.card.variant === "ai") {
        return "sidebar-ai-mark";
    }

    if (props.card.variant === "student") {
        return "sidebar-student-card-icon";
    }

    return "sidebar-extra-card-icon";
}

function getActionClass(): string[] {
    return [
        "sidebar-ai-btn",
        props.card.variant === "student" ? "sidebar-student-card-btn" : "",
    ].filter(Boolean);
}
</script>

<template>
    <div :class="getCardClass()">
        <div :class="getTopClass()">
            <div :class="getIconClass()">
                <img
                    v-if="card.image"
                    :src="card.image.src"
                    :alt="card.image.alt"
                />

                <i
                    v-else-if="card.icon"
                    :class="card.icon"
                ></i>
            </div>

            <div>
                <strong>{{ card.title }}</strong>
                <span>{{ card.subtitle }}</span>
            </div>
        </div>

        <p>{{ card.text }}</p>

        <RouterLink
            v-if="card.action.to"
            :class="getActionClass()"
            :to="card.action.to"
        >
            <i :class="card.action.icon"></i>
            {{ card.action.label }}
        </RouterLink>

        <a
            v-else
            :class="getActionClass()"
            :href="card.action.href || '#'"
        >
            <i :class="card.action.icon"></i>
            {{ card.action.label }}
        </a>
    </div>
</template>
