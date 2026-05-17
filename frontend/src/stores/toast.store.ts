import { computed, ref } from "vue";
import { defineStore } from "pinia";

export type ToastType = "success" | "error" | "warning" | "info";

export interface ToastItem {
    id: string;
    type: ToastType;
    title: string;
    message: string;
    duration: number;
}

interface ShowToastOptions {
    type?: ToastType;
    title?: string;
    message: string;
    duration?: number;
}

const DEFAULT_DURATION = 4200;

function createToastId(): string {
    return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export const useToastStore = defineStore("toast", () => {
    const items = ref<ToastItem[]>([]);

    const hasToasts = computed(() => items.value.length > 0);

    function removeToast(id: string): void {
        items.value = items.value.filter((toast) => toast.id !== id);
    }

    function showToast(options: ShowToastOptions): string {
        const id = createToastId();

        const toast: ToastItem = {
            id,
            type: options.type || "info",
            title: options.title || "",
            message: options.message,
            duration: options.duration ?? DEFAULT_DURATION,
        };

        items.value.push(toast);

        if (toast.duration > 0) {
            window.setTimeout(() => {
                removeToast(id);
            }, toast.duration);
        }

        return id;
    }

    function success(message: string, title = "Готово"): string {
        return showToast({
            type: "success",
            title,
            message,
        });
    }

    function error(message: string, title = "Ошибка"): string {
        return showToast({
            type: "error",
            title,
            message,
        });
    }

    function warning(message: string, title = "Проверьте данные"): string {
        return showToast({
            type: "warning",
            title,
            message,
        });
    }

    function info(message: string, title = "Информация"): string {
        return showToast({
            type: "info",
            title,
            message,
        });
    }

    function clearToasts(): void {
        items.value = [];
    }

    return {
        items,
        hasToasts,
        showToast,
        success,
        error,
        warning,
        info,
        removeToast,
        clearToasts,
    };
});