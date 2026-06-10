import { dashboardCreateModalContent } from "@/components/dashboard/data/dashboard-create-modal.data";

export const notesPageContent = {
    loadingText: "Загружаем заметки...",
    errorTitle: "Не удалось загрузить заметки",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    hero: {
        badge: "Личные заметки",
        title: "Заметки и напоминания",
        text:
            "Собирайте личные заметки по датам. Заметки отображаются в календаре и помогают видеть важные мысли рядом с планом на день.",
    },
    actions: {
        createLabel: "Создать заметку",
        deleteLabel: "Удалить заметку",
        openCalendarLabel: "Открыть календарь",
        readLabel: "Прочитать полностью",
        closeLabel: "Закрыть",
    },
    stats: {
        totalLabel: "Всего заметок",
        upcomingLabel: "Предстоящие",
        todayLabel: "На сегодня",
    },
    list: {
        title: "Все заметки",
        subtitle: "Заметки отсортированы по дате: сначала ближайшие и новые.",
        emptyTitle: "Заметок пока нет",
        emptyText: "Создайте первую заметку, и она появится здесь и на календаре выбранного дня.",
    },
    reader: {
        title: "Полный текст заметки",
    },
    modal: dashboardCreateModalContent,
} as const;
