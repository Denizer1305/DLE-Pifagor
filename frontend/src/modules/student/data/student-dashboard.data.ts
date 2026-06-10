export {
    dashboardCreateModalContent as studentCreateModalContent,
} from "@/components/dashboard/data/dashboard-create-modal.data";

export const studentDashboardPageUi = {
    loadingText: "Загружаем кабинет студента...",
    errorTitle: "Не удалось загрузить кабинет",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    emptyTitle: "Данные пока не добавлены",
    grades: {
        headers: [
            "Предмет",
            "Последняя работа",
            "Оценка",
            "Статус",
        ],
    },
} as const;

export const studentEmptyText = "Данные пока не добавлены";
