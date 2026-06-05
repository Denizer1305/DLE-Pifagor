import type { DashboardCreateItemModalContent } from "@/components/dashboard/types/dashboard.types";

export const dashboardCreateModalContent: DashboardCreateItemModalContent = {
    closeOverlayLabel: "Закрыть окно",
    closeButtonLabel: "Закрыть",
    cancelLabel: "Отмена",
    savingLabel: "Сохраняем...",
    calendar: {
        title: "Создать событие",
        description: "Добавьте событие в личный календарь.",
        titleLabel: "Название события",
        textLabel: "Описание",
        dateLabel: "Дата",
        eventTypeLabel: "Тема события",
        notificationLabel: "Уведомить в день события",
        notificationText: "Событие появится в уведомлениях в выбранную дату.",
        submitLabel: "Создать событие",
    },
    note: {
        title: "Создать заметку",
        description: "Добавьте личную заметку или напоминание.",
        titleLabel: "Заголовок заметки",
        textLabel: "Текст заметки",
        dateLabel: "Дата",
        eventTypeLabel: "",
        notificationLabel: "Создать напоминание",
        notificationText: "Заметка появится в уведомлениях в выбранную дату.",
        submitLabel: "Создать заметку",
    },
    calendarEventThemeOptions: [
        { value: "lesson", label: "Урок или занятие" },
        { value: "checking", label: "Проверка работ" },
        { value: "deadline", label: "Дедлайн" },
        { value: "system", label: "Организационное событие" },
        { value: "neutral", label: "Другое" },
    ],
};
