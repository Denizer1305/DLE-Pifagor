<script setup lang="ts">
import { useRouter } from "vue-router";

import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { ROLE_LABELS } from "@/app/constants/roles.constants";

import NotificationFeed from "@/modules/notifications/components/NotificationFeed.vue";
import NotificationPageHeader from "@/modules/notifications/components/NotificationPageHeader.vue";
import NotificationStatusTabs from "@/modules/notifications/components/NotificationStatusTabs.vue";

import {
    notificationCategoryOptions,
    notificationLevelOptions,
    notificationStatusOptions,
} from "@/modules/notifications/data/notification-options.data";
import { useNotificationFeed } from "@/modules/notifications/composables/useNotificationFeed";
import { createSettingsScaffold } from "@/modules/settings/mappers/settings.mapper";
import { redirectToLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

import type {
    NotificationCategory,
    NotificationLevel,
    NotificationStatus,
} from "@/modules/notifications/types/notifications.types";

const router = useRouter();
const authStore = useAuthStore();

const {
    filters,
    items,
    unreadCount,
    isLoading,
    isActionLoading,
    errorMessage,
    loadFeed,
    updateFilter,
    markAsRead,
    markAllAsRead,
    complete,
    remove,
} = useNotificationFeed();

const scaffold = createSettingsScaffold(
    {
        fullName: authStore.userFullName || "Пользователь",
            roleLabel: authStore.activeRole
                ? ROLE_LABELS[authStore.activeRole]
                : "Пользователь",
            roleCode: authStore.activeRole || "",
            avatarUrl: authStore.avatarUrl || ""
    },
    "notifications-page",
);

async function logout(): Promise<void> {
    if (!authStore.isAuthenticated) {
        return;
    }

    await redirectToLogout(router);
}
</script>

<template>
    <DashboardPageScaffold
        :model="scaffold"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем уведомления..."
        @reload="loadFeed"
        @logout="logout"
    >
        <NotificationPageHeader
            :unread-count="unreadCount"
            :is-loading="isLoading"
            :disabled="isActionLoading"
            @read-all="markAllAsRead"
            @reload="loadFeed"
        />

        <section class="notification-page-filters fade-in visible">
            <NotificationStatusTabs
                :model-value="filters.status || ''"
                :options="notificationStatusOptions"
                :disabled="isLoading"
                @update:model-value="updateFilter('status', $event as NotificationStatus | '')"
            />

            <div class="notification-page-filter-grid">
                <div class="notification-page-filter-field">
                    <span>Категория</span>
                    <BaseSelect
                        :model-value="filters.category || ''"
                        :options="notificationCategoryOptions"
                        aria-label="Выбрать категорию уведомлений"
                        :disabled="isLoading"
                        @update:model-value="updateFilter('category', $event as NotificationCategory | '')"
                    />
                </div>

                <div class="notification-page-filter-field">
                    <span>Важность</span>
                    <BaseSelect
                        :model-value="filters.level || ''"
                        :options="notificationLevelOptions"
                        aria-label="Выбрать важность уведомлений"
                        :disabled="isLoading"
                        @update:model-value="updateFilter('level', $event as NotificationLevel | '')"
                    />
                </div>
            </div>
        </section>

        <NotificationFeed
            :items="items"
            :is-loading="isLoading"
            :disabled="isActionLoading"
            @read="markAsRead"
            @complete="complete"
            @remove="remove"
        />
    </DashboardPageScaffold>
</template>
