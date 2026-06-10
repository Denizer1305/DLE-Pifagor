export {
    dashboardCreateModalContent as parentCreateModalContent,
} from "@/components/dashboard/data/dashboard-create-modal.data";

export const parentDashboardPageUi = {
    loadingText: "Загружаем кабинет родителя...",
    errorTitle: "Не удалось загрузить кабинет",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    emptyTitle: "Данные пока не добавлены",
    courses: {
        filters: [
            "Все",
            "Основные",
            "С заданиями",
        ],
    },
    grades: {
        headers: [
            "Предмет",
            "Последняя работа",
            "Оценка",
            "Статус",
        ],
    },
} as const;

export const parentEmptyText = "Данные пока не добавлены";
