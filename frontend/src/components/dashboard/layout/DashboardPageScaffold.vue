<script setup lang="ts">
import { computed } from "vue";

import DashboardCalendar from "@/components/dashboard/calendar/DashboardCalendar.vue";
import { useDashboardCreateItems } from "@/components/dashboard/composables/useDashboardCreateItems";
import { useDashboardSidebar } from "@/composables/dashboard/useDashboardSidebar";
import DashboardShell from "@/components/dashboard/layout/DashboardShell.vue";
import DashboardCreateItemModal from "@/components/dashboard/panels/DashboardCreateItemModal.vue";
import DashboardNotesPanel from "@/components/dashboard/panels/DashboardNotesPanel.vue";
import DashboardNotificationsPanel from "@/components/dashboard/panels/DashboardNotificationsPanel.vue";
import DashboardProfilePanel from "@/components/dashboard/panels/DashboardProfilePanel.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import type { DashboardPageScaffoldModel } from "@/components/dashboard/types/dashboard.types";

interface Props {
    model: DashboardPageScaffoldModel;
    isLoading: boolean;
    errorMessage: string;
    loadingText: string;
    errorTitle?: string;
    retryLabel?: string;
    retryIcon?: string;
}

interface Emits {
    (event: "reload"): void;
    (event: "logout"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const modelSource = computed(() => props.model);

const {
    isSidebarOpen,
    closeSidebar,
    toggleSidebar,
} = useDashboardSidebar();

const {
    calendarDays,
    createModalKind,
    isCreateModalOpen,
    notesContent,
    closeCreateModal,
    openCreateModal,
    submitCreateModal,
} = useDashboardCreateItems(modelSource);
</script>

<template>
    <DashboardShell
        :config="model.shell"
        :is-sidebar-open="isSidebarOpen"
        @toggle-sidebar="toggleSidebar"
        @close-sidebar="closeSidebar"
    >
        <template #calendar>
            <DashboardCalendar
                :content="model.calendarContent"
                :days="calendarDays"
                @create="openCreateModal('calendar')"
            />
        </template>

        <template #notifications>
            <DashboardNotificationsPanel
                :content="model.notifications"
            />
        </template>

        <template #notes>
            <DashboardNotesPanel
                :content="notesContent"
                @create="openCreateModal('note')"
            />
        </template>

        <template #profile>
            <DashboardProfilePanel
                :content="model.profilePanel"
                @logout="emit('logout')"
            />
        </template>

        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="loadingText"
        />

        <DashboardStateView
            v-else-if="errorMessage"
            variant="error"
            :title="errorTitle"
            :text="errorMessage"
            :action-label="retryLabel"
            :action-icon="retryIcon"
            @action="emit('reload')"
        />

        <template v-else>
            <slot></slot>
        </template>

        <DashboardCreateItemModal
            v-if="model.createModal"
            :is-open="isCreateModalOpen"
            :kind="createModalKind"
            :content="model.createModal"
            @close="closeCreateModal"
            @submit="submitCreateModal"
        />
    </DashboardShell>
</template>
