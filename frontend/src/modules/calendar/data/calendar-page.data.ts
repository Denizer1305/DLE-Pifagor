import { dashboardCreateModalContent } from "@/components/dashboard/data/dashboard-create-modal.data";

export const calendarPageContent = {
    loadingText: "Загружаем календарь...",
    errorTitle: "Не удалось загрузить календарь",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    hero: {
        badge: "Личный календарь",
        title: "План на день",
        text:
            "Выберите дату, добавьте события и соберите рабочий план. Сохранённые события появятся в календаре на главной странице личного кабинета.",
    },
    calendar: {
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        emptyDayTitle: "План на день пуст",
        emptyDayText: "Добавьте первое событие, чтобы оно появилось в календаре личного кабинета.",
        selectedDayLabel: "Выбранный день",
        eventsTitle: "План на день",
        createTitle: "Добавить событие",
        deleteLabel: "Удалить",
    },
    form: {
        titleLabel: dashboardCreateModalContent.calendar.titleLabel,
        titlePlaceholder: "Например: консультация по проекту",
        textLabel: dashboardCreateModalContent.calendar.textLabel,
        textPlaceholder: "Кратко опишите задачу, встречу или напоминание.",
        dateLabel: dashboardCreateModalContent.calendar.dateLabel,
        eventTypeLabel: dashboardCreateModalContent.calendar.eventTypeLabel,
        notificationLabel: dashboardCreateModalContent.calendar.notificationLabel,
        notificationText: dashboardCreateModalContent.calendar.notificationText,
        submitLabel: "Добавить в план",
        savingLabel: dashboardCreateModalContent.savingLabel,
    },
    eventTypeOptions: dashboardCreateModalContent.calendarEventThemeOptions,
    legendHint: "Это пример обозначений тем событий. Реальные события появятся в календаре после добавления плана на выбранный день.",
    legend: dashboardCreateModalContent.calendarEventThemeOptions.map((option) => ({
        key: option.value,
        label: option.label,
    })),
} as const;
