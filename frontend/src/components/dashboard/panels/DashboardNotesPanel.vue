<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { DashboardNotesContent } from "@/components/dashboard/types/dashboard.types";

interface Props {
    content: DashboardNotesContent;
}

defineProps<Props>();
const emit = defineEmits<{
    (event: "create"): void;
}>();
</script>

<template>
    <div class="dashboard-panel-content">
        <div class="dashboard-floating-panel-head">
            <strong>{{ content.title }}</strong>
        </div>

        <button
            type="button"
            class="dashboard-panel-create-btn"
            @click="emit('create')"
        >
            <i class="fas fa-plus"></i>
            {{ content.createLabel }}
        </button>

        <div
            v-if="content.items.length"
            class="dashboard-notes-list"
        >
            <div
                v-for="item in content.items"
                :key="item.id"
                class="dashboard-note-item"
            >
                <div class="dashboard-note-date">
                    {{ item.date }}
                </div>

                <div class="dashboard-note-body">
                    <strong>{{ item.title }}</strong>
                    <span>{{ item.text }}</span>
                </div>
            </div>
        </div>

        <div
            v-else
            class="dashboard-panel-empty"
        >
            {{ content.emptyText }}
        </div>

        <RouterLink
            v-if="content.actionTo"
            class="dashboard-panel-link"
            :to="content.actionTo"
        >
            {{ content.actionLabel }}
        </RouterLink>

        <a
            v-else-if="content.actionLabel"
            href="#"
            class="dashboard-panel-link"
        >
            {{ content.actionLabel }}
        </a>
    </div>
</template>
