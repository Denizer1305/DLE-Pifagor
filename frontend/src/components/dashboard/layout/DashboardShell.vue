<script setup lang="ts">
import DashboardSidebar from "@/components/dashboard/layout/DashboardSidebar.vue";
import DashboardTopbar from "@/components/dashboard/layout/DashboardTopbar.vue";
import type { DashboardShellConfig } from "@/components/dashboard/types/dashboard.types";

interface Props {
    config: DashboardShellConfig;
    isSidebarOpen?: boolean;
    notesCount?: number;
}

interface Emits {
    (event: "toggle-sidebar"): void;
    (event: "close-sidebar"): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>

<template>
    <div :class="config.pageClass">
        <div
            class="dashboard-sidebar-overlay"
            :class="{ 'is-active': isSidebarOpen }"
            @click="$emit('close-sidebar')"
        ></div>

        <div class="dashboard-shell">
            <DashboardSidebar
                :brand="config.brand"
                :profile="config.profile"
                :navigation="config.navigation"
                :extra-card="config.sidebarExtra"
                :is-open="isSidebarOpen"
            />

            <main class="dashboard-main">
                <div class="dashboard-main-inner">
                    <DashboardTopbar
                        :search="config.search"
                        :labels="config.topbarLabels"
                        :user="config.topbarUser"
                        :notes-count="notesCount"
                        @toggle-sidebar="$emit('toggle-sidebar')"
                    >
                        <template #calendar>
                            <slot name="calendar"></slot>
                        </template>

                        <template #notifications>
                            <slot name="notifications"></slot>
                        </template>

                        <template #notes>
                            <slot name="notes"></slot>
                        </template>

                        <template #profile>
                            <slot name="profile"></slot>
                        </template>
                    </DashboardTopbar>

                    <slot></slot>
                </div>
            </main>
        </div>
    </div>
</template>
