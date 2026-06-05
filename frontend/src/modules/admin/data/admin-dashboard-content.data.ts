import type {
    DashboardAiCardContent,
    DashboardDayCardContent,
    DashboardIntroContent,
} from "@/components/dashboard/types/dashboard.types";

import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";

export const adminIntroContent: DashboardIntroContent = {
    badges: [
        {
            label: "Административная панель",
            icon: "fas fa-shield-halved",
        },
        {
            label: "ЦОС «Пифагор»",
            icon: "fas fa-layer-group",
        },
    ],
    title: "Центр управления платформой",
    text:
        "Здесь собраны ключевые показатели системы: пользователи, подключения, курсы, обращения, модерация и контрольные события.",
    actions: [
        {
            label: "Добавить пользователя",
            icon: "fas fa-user-plus",
            to: {
                name: "admin-users-create",
            },
            variant: "primary",
        },
        {
            label: "Создать курс",
            icon: "fas fa-book-open",
            to: {
                name: "admin-courses-create",
            },
            variant: "secondary",
        },
        {
            label: "Открыть обращения",
            icon: "fas fa-envelope-open-text",
            to: {
                name: "admin-feedback",
            },
            variant: "secondary",
        },
    ],
};

export const adminDayCardContent: DashboardDayCardContent = {
    badge: "Сегодня",
    icon: "fas fa-calendar-day",
    title: "Сегодня",
    text:
        "Важно проверить обращения, просмотреть системные события, подтвердить новые заявки и обновить ключевые данные.",
    stats: [
        {
            value: 0,
            label: "новых заявок",
        },
        {
            value: 0,
            label: "событий",
        },
        {
            value: 0,
            label: "на контроле",
        },
    ],
};

export const adminAiCardContent: DashboardAiCardContent = {
    image: {
        src: anastasiaLogo,
        alt: "Анастасия",
    },
    title: "Анастасия",
    subtitle: "ИИ-помощник администратора",
    text:
        "Я могу помочь с анализом активности, составить управленческую сводку, выделить проблемные участки платформы или предложить приоритеты на день.",
    action: {
        label: "Проанализировать платформу",
        icon: "fas fa-chart-line",
        to: {
            name: "admin-dashboard",
        },
        variant: "primary",
    },
    actions: [
        {
            label: "Проанализировать платформу",
            icon: "fas fa-chart-line",
            to: {
                name: "admin-dashboard",
            },
        },
        {
            label: "Найти проблемные группы",
            icon: "fas fa-users",
            to: {
                name: "admin-analytics",
            },
        },
        {
            label: "Сгруппировать обращения",
            icon: "fas fa-envelope-open-text",
            to: {
                name: "admin-feedback",
            },
        },
        {
            label: "Сформировать сводку",
            icon: "fas fa-file-lines",
            to: {
                name: "admin-system",
            },
        },
    ],
};
