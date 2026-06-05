<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import type {
    DashboardSearchConfig,
    DashboardTopbarLabels,
    DashboardTopbarUser,
} from "@/components/dashboard/types/dashboard.types";
import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";

interface Props {
    search: DashboardSearchConfig;
    labels: DashboardTopbarLabels;
    user: DashboardTopbarUser;
}

interface Emits {
    (event: "toggle-sidebar"): void;
}

defineProps<Props>();
defineEmits<Emits>();

const notificationsStore = useNotificationsStore();
const activePanel = ref<string | null>(null);
const unreadCount = computed(() => notificationsStore.unreadCount);

function togglePanel(panelName: string): void {
    activePanel.value = activePanel.value === panelName
        ? null
        : panelName;

    if (activePanel.value === "notifications") {
        void notificationsStore.loadFeed();
        void notificationsStore.loadUnreadCount();
    }
}

function closePanels(): void {
    activePanel.value = null;
}

onMounted(() => {
    void notificationsStore.loadUnreadCount();
});
</script>

<template>
    <div class="teacher-dashboard-topbar">
        <button
            class="dashboard-mobile-menu-btn"
            type="button"
            :aria-label="labels.menu"
            @click="$emit('toggle-sidebar')"
        >
            <i class="fas fa-bars"></i>
        </button>

        <div class="teacher-dashboard-search">
            <i class="fas fa-search"></i>

            <input
                type="text"
                :placeholder="search.placeholder"
                :aria-label="search.ariaLabel"
            />
        </div>

        <div class="teacher-dashboard-topbar-actions">
            <div class="dashboard-header-control">
                <button
                    class="dashboard-icon-btn is-calendar"
                    type="button"
                    data-dashboard-panel-toggle="calendar"
                    :aria-label="labels.calendar"
                    :aria-expanded="activePanel === 'calendar'"
                    @click="togglePanel('calendar')"
                >
                    <i class="fas fa-calendar-alt"></i>
                </button>

                <div
                    v-if="activePanel === 'calendar'"
                    class="dashboard-floating-panel dashboard-calendar-panel is-open"
                    data-dashboard-panel="calendar"
                >
                    <slot name="calendar"></slot>
                </div>
            </div>

            <div class="dashboard-header-control">
                <button
                    class="dashboard-icon-btn"
                    type="button"
                    data-dashboard-panel-toggle="notifications"
                    :aria-label="labels.notifications"
                    :aria-expanded="activePanel === 'notifications'"
                    @click="togglePanel('notifications')"
                >
                    <i class="fas fa-bell"></i>
                    <span
                        v-if="unreadCount"
                        class="dashboard-icon-badge"
                    >
                        {{ unreadCount > 99 ? "99+" : unreadCount }}
                    </span>
                </button>

                <div
                    v-if="activePanel === 'notifications'"
                    class="dashboard-floating-panel dashboard-notifications-panel is-open"
                    data-dashboard-panel="notifications"
                >
                    <slot name="notifications"></slot>
                </div>
            </div>

            <div class="dashboard-header-control">
                <button
                    class="dashboard-icon-btn"
                    type="button"
                    data-dashboard-panel-toggle="notes"
                    :aria-label="labels.notes"
                    :aria-expanded="activePanel === 'notes'"
                    @click="togglePanel('notes')"
                >
                    <i class="fas fa-note-sticky"></i>
                </button>

                <div
                    v-if="activePanel === 'notes'"
                    class="dashboard-floating-panel dashboard-notes-panel is-open"
                    data-dashboard-panel="notes"
                >
                    <slot name="notes"></slot>
                </div>
            </div>

            <div class="dashboard-header-control dashboard-profile-control">
                <button
                    class="teacher-dashboard-user"
                    type="button"
                    data-dashboard-panel-toggle="profile"
                    :aria-label="labels.profile"
                    :aria-expanded="activePanel === 'profile'"
                    @click="togglePanel('profile')"
                >
                    <div class="teacher-dashboard-user-avatar">
                        <img
                            v-if="user.avatarUrl"
                            :src="user.avatarUrl"
                            :alt="user.avatarAlt"
                        />

                        <span v-else>
                            {{ user.fullName.slice(0, 1).toUpperCase() }}
                        </span>
                    </div>

                    <div class="teacher-dashboard-user-meta">
                        <strong>{{ user.fullName }}</strong>
                        <span>{{ user.roleLabel }}</span>
                    </div>
                </button>

                <div
                    v-if="activePanel === 'profile'"
                    class="dashboard-floating-panel dashboard-profile-panel is-open"
                    data-dashboard-panel="profile"
                >
                    <slot name="profile"></slot>
                </div>
            </div>
        </div>

        <button
            v-if="activePanel"
            class="dashboard-panel-backdrop"
            type="button"
            :aria-label="labels.closePanel"
            @click="closePanels"
        ></button>
    </div>
</template>
