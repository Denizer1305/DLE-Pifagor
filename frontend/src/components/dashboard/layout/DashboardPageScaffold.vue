<script setup lang="ts">
import { computed, onMounted } from "vue";

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
import type { DashboardCreateItemKind } from "@/components/dashboard/types/dashboard.types";
import { getNotificationActionTarget } from "@/modules/notifications/mappers/notification.mapper";
import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";

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
const notificationsStore = useNotificationsStore();
const notificationsContent = computed(() => {
    return {
        ...props.model.notifications,
        count: notificationsStore.unreadCount,
        countLabel: props.model.notifications.countLabel || "новых",
        items: notificationsStore.unreadItems
            .slice(0, 6)
            .map((item) => ({
                id: item.id,
                title: item.title,
                text: item.message,
                icon: item.levelIcon,
                isNew: item.isUnread,
                actionLabel: item.actionLabel,
                actionTo: item.hasAction
                    ? getNotificationActionTarget(item.actionUrl)
                    : undefined,
            })),
    };
});

const {
    isSidebarOpen,
    closeSidebar,
    toggleSidebar,
} = useDashboardSidebar();

const {
    calendarDays,
    createModalKind,
    isCreateModalOpen,
    isSaving,
    notesContent,
    saveError,
    closeCreateModal,
    deleteItem,
    openCreateModal,
    submitCreateModal,
} = useDashboardCreateItems(modelSource);

async function handleCreateItem(payload: Parameters<typeof submitCreateModal>[0]): Promise<void> {
    const wasSaved = await submitCreateModal(payload);

    if (wasSaved && payload.notificationEnabled) {
        emit("reload");
    }
}

async function handleDeleteItem(itemId: number): Promise<void> {
    if (await deleteItem(itemId)) {
        emit("reload");
    }
}

function handleOpenNotification(notificationId: string | number): void {
    const normalizedId = Number(notificationId);

    if (Number.isFinite(normalizedId)) {
        void notificationsStore.markAsRead(normalizedId);
    }
}

function openCreateItem(kind: DashboardCreateItemKind): void {
    openCreateModal(kind);
}

defineExpose({
    openCreateItem,
});

onMounted(() => {
    void notificationsStore.loadFeed();
});
</script>

<template>
    <DashboardShell
        :config="model.shell"
        :is-sidebar-open="isSidebarOpen"
        :notes-count="notesContent.count"
        @toggle-sidebar="toggleSidebar"
        @close-sidebar="closeSidebar"
    >
        <template #calendar>
            <DashboardCalendar
                :content="model.calendarContent"
                :days="calendarDays"
                @create="openCreateModal('calendar')"
                @remove="handleDeleteItem"
            />
        </template>

        <template #notifications>
            <DashboardNotificationsPanel
                :content="notificationsContent"
                @open="handleOpenNotification"
            />
        </template>

        <template #notes>
            <DashboardNotesPanel
                :content="notesContent"
                @create="openCreateModal('note')"
                @remove="handleDeleteItem"
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
            :is-submitting="isSaving"
            :error-message="saveError"
            @close="closeCreateModal"
            @submit="handleCreateItem"
        />
    </DashboardShell>
</template>
