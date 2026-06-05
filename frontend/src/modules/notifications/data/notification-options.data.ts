import type {
    NotificationCategory,
    NotificationFilterOption,
    NotificationLevel,
    NotificationStatus,
} from "@/modules/notifications/types/notifications.types";

export const notificationStatusOptions: NotificationFilterOption[] = [
    {
        value: "",
        label: "Все",
        icon: "fas fa-layer-group",
    },
    {
        value: "unread",
        label: "Непрочитанные",
        icon: "fas fa-envelope",
    },
    {
        value: "read",
        label: "Прочитанные",
        icon: "fas fa-envelope-open",
    },
    {
        value: "completed",
        label: "Выполненные",
        icon: "fas fa-circle-check",
    },
];

export const notificationLevelOptions: NotificationFilterOption[] = [
    {
        value: "",
        label: "Все уровни",
        icon: "fas fa-signal",
    },
    {
        value: "info",
        label: "Информация",
        icon: "fas fa-circle-info",
    },
    {
        value: "success",
        label: "Успешные",
        icon: "fas fa-circle-check",
    },
    {
        value: "warning",
        label: "Предупреждения",
        icon: "fas fa-triangle-exclamation",
    },
    {
        value: "danger",
        label: "Критичные",
        icon: "fas fa-shield-halved",
    },
];

export const notificationCategoryOptions: NotificationFilterOption[] = [
    {
        value: "",
        label: "Все категории",
        icon: "fas fa-layer-group",
    },
    {
        value: "daily_summary",
        label: "Сводка",
        icon: "fas fa-calendar-day",
    },
    {
        value: "assignments",
        label: "Задания",
        icon: "fas fa-clipboard-list",
    },
    {
        value: "tests",
        label: "Контрольные",
        icon: "fas fa-file-circle-check",
    },
    {
        value: "schedule",
        label: "Расписание",
        icon: "fas fa-calendar-days",
    },
    {
        value: "calendar",
        label: "Календарь",
        icon: "fas fa-calendar-check",
    },
    {
        value: "notes",
        label: "Заметки",
        icon: "fas fa-note-sticky",
    },
    {
        value: "birthday",
        label: "День рождения",
        icon: "fas fa-cake-candles",
    },
    {
        value: "feedback",
        label: "Поддержка",
        icon: "fas fa-headset",
    },
    {
        value: "moderation",
        label: "Модерация",
        icon: "fas fa-user-shield",
    },
    {
        value: "security",
        label: "Безопасность",
        icon: "fas fa-shield-halved",
    },
    {
        value: "system",
        label: "Система",
        icon: "fas fa-gear",
    },
];

export const notificationLevelLabels: Record<NotificationLevel, string> = {
    info: "Информация",
    success: "Успешное событие",
    warning: "Предупреждение",
    danger: "Критичное",
};

export const notificationLevelIcons: Record<NotificationLevel, string> = {
    info: "fas fa-circle-info",
    success: "fas fa-circle-check",
    warning: "fas fa-triangle-exclamation",
    danger: "fas fa-shield-halved",
};

export const notificationStatusLabels: Record<NotificationStatus, string> = {
    unread: "Не прочитано",
    read: "Прочитано",
    completed: "Выполнено",
    archived: "В архиве",
};

export const notificationCategoryLabels: Record<NotificationCategory, string> = {
    daily_summary: "Ежедневная сводка",
    assignments: "Задания",
    tests: "Контрольные и экзамены",
    schedule: "Расписание",
    calendar: "Календарь",
    notes: "Заметки",
    birthday: "День рождения",
    education: "Образование",
    feedback: "Обратная связь",
    moderation: "Модерация",
    security: "Безопасность",
    system: "Система",
};