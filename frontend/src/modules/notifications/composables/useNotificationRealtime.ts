import { onBeforeUnmount, ref } from "vue";

import { useNotificationsStore } from "@/modules/notifications/stores/notifications.store";
import type { NotificationRealtimeMessage } from "@/modules/notifications/types/notifications.types";

interface RealtimeOptions {
    autoReconnect?: boolean;
    reconnectDelay?: number;
}

export function useNotificationRealtime(options: RealtimeOptions = {}) {
    const notificationsStore = useNotificationsStore();

    const socket = ref<WebSocket | null>(null);
    const isConnected = ref(false);
    const errorMessage = ref("");

    const autoReconnect = options.autoReconnect ?? true;
    const reconnectDelay = options.reconnectDelay ?? 3000;

    let reconnectTimer: number | null = null;
    let isClosedManually = false;

    function connect(): void {
        if (socket.value && socket.value.readyState === WebSocket.OPEN) {
            return;
        }

        isClosedManually = false;
        errorMessage.value = "";

        const url = buildNotificationWebSocketUrl();

        socket.value = new WebSocket(url);

        socket.value.onopen = () => {
            isConnected.value = true;
        };

        socket.value.onmessage = (event) => {
            handleSocketMessage(event.data);
        };

        socket.value.onerror = () => {
            errorMessage.value = "Ошибка WebSocket-соединения уведомлений.";
        };

        socket.value.onclose = () => {
            isConnected.value = false;

            if (autoReconnect && !isClosedManually) {
                scheduleReconnect();
            }
        };
    }

    function disconnect(): void {
        isClosedManually = true;

        if (reconnectTimer) {
            window.clearTimeout(reconnectTimer);
            reconnectTimer = null;
        }

        if (socket.value) {
            socket.value.close();
            socket.value = null;
        }

        isConnected.value = false;
    }

    function scheduleReconnect(): void {
        if (reconnectTimer) {
            return;
        }

        reconnectTimer = window.setTimeout(() => {
            reconnectTimer = null;
            connect();
        }, reconnectDelay);
    }

    function handleSocketMessage(rawMessage: string): void {
        try {
            const message = JSON.parse(rawMessage) as NotificationRealtimeMessage;

            notificationsStore.applyRealtimeMessage(message);
        } catch (_error) {
            errorMessage.value = "Не удалось обработать WebSocket-сообщение.";
        }
    }

    onBeforeUnmount(() => {
        disconnect();
    });

    return {
        isConnected,
        errorMessage,
        connect,
        disconnect,
    };
}

function buildNotificationWebSocketUrl(): string {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const host = window.location.host;

    return `${protocol}://${host}/ws/notifications/`;
}