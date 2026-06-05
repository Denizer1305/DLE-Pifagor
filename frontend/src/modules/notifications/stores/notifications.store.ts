import { defineStore } from "pinia";

import { mapNotificationFeedDtoToViewModel } from "@/modules/notifications/mappers/notification.mapper";
import {
    finishNotification,
    getNotifications,
    getUnreadNotificationCount,
    readAllNotifications,
    readNotification,
    removeNotification,
    runNotificationBootstrap,
} from "@/modules/notifications/services/notifications.service";
import type {
    NotificationBootstrapPayload,
    NotificationQueryParams,
    NotificationRealtimeMessage,
    NotificationViewModel,
} from "@/modules/notifications/types/notifications.types";
import { mapNotificationDtoToViewModel } from "@/modules/notifications/mappers/notification.mapper";

interface NotificationsState {
    items: NotificationViewModel[];
    unreadCount: number;
    isLoading: boolean;
    isBootstrapping: boolean;
    isActionLoading: boolean;
    errorMessage: string;
    lastBootstrapDate: string;
}

export const useNotificationsStore = defineStore("notifications", {
    state: (): NotificationsState => ({
        items: [],
        unreadCount: 0,
        isLoading: false,
        isBootstrapping: false,
        isActionLoading: false,
        errorMessage: "",
        lastBootstrapDate: "",
    }),

    getters: {
        unreadItems(state): NotificationViewModel[] {
            return state.items.filter((item) => item.isUnread);
        },

        importantItems(state): NotificationViewModel[] {
            return state.items.filter((item) => {
                return item.level === "warning" || item.level === "danger";
            });
        },

        latestItems(state): NotificationViewModel[] {
            return state.items.slice(0, 6);
        },

        hasUnread(state): boolean {
            return state.unreadCount > 0;
        },
    },

    actions: {
        async bootstrap(
            payload: NotificationBootstrapPayload = {
                reason: "dashboard_login",
            },
        ): Promise<void> {
            this.isBootstrapping = true;
            this.errorMessage = "";

            try {
                const response = await runNotificationBootstrap(payload);

                this.lastBootstrapDate = response.target_date;
                this.unreadCount = response.unread_count;

                await this.loadFeed();
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            } finally {
                this.isBootstrapping = false;
            }
        },

        async loadFeed(params: NotificationQueryParams = {}): Promise<void> {
            this.isLoading = true;
            this.errorMessage = "";

            try {
                const response = await getNotifications(params);
                const viewModel = mapNotificationFeedDtoToViewModel(response);

                this.items = viewModel.items;
                this.unreadCount = viewModel.unreadCount;
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            } finally {
                this.isLoading = false;
            }
        },

        async loadUnreadCount(): Promise<void> {
            try {
                const response = await getUnreadNotificationCount();

                this.unreadCount = response.unread_count;
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            }
        },

        async markAsRead(notificationId: number): Promise<void> {
            this.isActionLoading = true;
            this.errorMessage = "";

            try {
                const response = await readNotification(notificationId);
                const item = mapNotificationDtoToViewModel(response.notification);

                this.replaceItem(item);
                await this.loadUnreadCount();
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            } finally {
                this.isActionLoading = false;
            }
        },

        async markAllAsRead(): Promise<void> {
            this.isActionLoading = true;
            this.errorMessage = "";

            try {
                const response = await readAllNotifications();

                this.unreadCount = response.unread_count;
                this.items = this.items.map((item) => ({
                    ...item,
                    status: "read",
                    statusLabel: "Прочитано",
                    isUnread: false,
                }));
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            } finally {
                this.isActionLoading = false;
            }
        },

        async complete(notificationId: number): Promise<void> {
            this.isActionLoading = true;
            this.errorMessage = "";

            try {
                const response = await finishNotification(notificationId);
                const item = mapNotificationDtoToViewModel(response.notification);

                this.replaceItem(item);
                await this.loadUnreadCount();
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            } finally {
                this.isActionLoading = false;
            }
        },

        async remove(notificationId: number): Promise<void> {
            this.isActionLoading = true;
            this.errorMessage = "";

            try {
                await removeNotification(notificationId);

                this.items = this.items.filter((item) => item.id !== notificationId);
                await this.loadUnreadCount();
                window.dispatchEvent(new Event("dashboard-items:changed"));
            } catch (error) {
                this.errorMessage = getNotificationErrorMessage(error);
            } finally {
                this.isActionLoading = false;
            }
        },

        applyRealtimeMessage(message: NotificationRealtimeMessage): void {
            if (typeof message.unread_count === "number") {
                this.unreadCount = message.unread_count;
            }

            if (message.type === "notification.created" && message.notification) {
                const item = mapNotificationDtoToViewModel(message.notification);

                this.items = [
                    item,
                    ...this.items.filter((current) => current.id !== item.id),
                ];

                return;
            }

            if (
                message.type === "notification.deleted" &&
                typeof message.notification_id === "number"
            ) {
                this.items = this.items.filter((item) => {
                    return item.id !== message.notification_id;
                });
            }
        },

        replaceItem(nextItem: NotificationViewModel): void {
            const index = this.items.findIndex((item) => item.id === nextItem.id);

            if (index === -1) {
                this.items = [
                    nextItem,
                    ...this.items,
                ];

                return;
            }

            this.items.splice(index, 1, nextItem);
        },

        reset(): void {
            this.items = [];
            this.unreadCount = 0;
            this.isLoading = false;
            this.isBootstrapping = false;
            this.isActionLoading = false;
            this.errorMessage = "";
            this.lastBootstrapDate = "";
        },
    },
});

function getNotificationErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось выполнить действие с уведомлениями.";
}
