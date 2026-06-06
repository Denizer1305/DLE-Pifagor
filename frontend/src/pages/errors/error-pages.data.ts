import type { RouteLocationRaw } from "vue-router";

export interface ErrorPageAction {
    label: string;
    icon: string;
    to?: RouteLocationRaw;
    variant?: "primary" | "secondary" | "info";
    action?: "back";
}

export interface ErrorPageDetails {
    title: string;
    icon: string;
    items: string[];
}

export interface ErrorPageQuickLink {
    title: string;
    description: string;
    icon: string;
    to: RouteLocationRaw;
}

export interface ErrorPageNote {
    text: string;
    icon: string;
    tone?: "warning" | "info";
}

export interface ErrorPageContent {
    code: string;
    variant: "forbidden" | "not-found";
    title: string;
    subtitle: string;
    description: string;
    details?: ErrorPageDetails;
    quickLinks?: ErrorPageQuickLink[];
    notes: ErrorPageNote[];
    visualIcon: string;
    orbitIcon: string;
    actions: ErrorPageAction[];
    footer: {
        text: string;
        address: string;
        email: string;
        phone: string;
    };
}

const commonFooter = {
    text: "Цифровая образовательная среда «Пифагор»",
    address: "Владимирская область, г. Владимир",
    email: "Pifagor-Platform33@yandex.ru",
    phone: "+7 (900) 000-00-00",
};

export const forbiddenPageContent: ErrorPageContent = {
    code: "403",
    variant: "forbidden",
    title: "Доступ запрещён",
    subtitle: "У вас недостаточно прав для доступа к этому ресурсу.",
    description: "Запрошенная страница или действие требуют специальных разрешений. ЦОС «Пифагор» защищает данные пользователей, учебные материалы и административные разделы платформы.",
    details: {
        title: "Почему доступ ограничен?",
        icon: "fa-solid fa-ban",
        items: [
            "Ресурс доступен только определённым группам пользователей.",
            "Требуется более высокая роль или уровень доступа.",
            "Вы пытаетесь открыть защищённый раздел личного кабинета.",
            "Раздел временно ограничен администратором образовательной организации.",
            "Необходимо подтверждение учётной записи.",
        ],
    },
    notes: [
        {
            text: "Если вы считаете, что это ошибка, обратитесь к администратору вашего учебного заведения.",
            icon: "fa-solid fa-triangle-exclamation",
            tone: "warning",
        },
    ],
    visualIcon: "fa-solid fa-lock",
    orbitIcon: "fa-solid fa-shield-halved",
    actions: [
        {
            label: "На главную",
            icon: "fa-solid fa-house",
            to: { name: "home" },
            variant: "primary",
        },
        {
            label: "Вернуться назад",
            icon: "fa-solid fa-arrow-left",
            action: "back",
            variant: "secondary",
        },
    ],
    footer: commonFooter,
};

export const notFoundPageContent: ErrorPageContent = {
    code: "404",
    variant: "not-found",
    title: "Страница не найдена",
    subtitle: "Запрашиваемая страница не существует или была перемещена.",
    description: "Возможно, вы ввели неправильный адрес, или раздел был переименован. Попробуйте перейти в один из актуальных публичных разделов ЦОС «Пифагор».",
    quickLinks: [
        {
            title: "Главная страница",
            description: "Начните с главной страницы платформы.",
            icon: "fa-solid fa-house",
            to: { name: "home" },
        },
        {
            title: "Преподаватели",
            description: "Посмотрите преподавателей образовательной среды.",
            icon: "fa-solid fa-chalkboard-user",
            to: { name: "teachers" },
        },
        {
            title: "Личный кабинет",
            description: "Войдите в пространство студента, родителя, преподавателя или администратора.",
            icon: "fa-solid fa-right-to-bracket",
            to: { name: "login" },
        },
        {
            title: "Контакты",
            description: "Свяжитесь с командой платформы.",
            icon: "fa-solid fa-headset",
            to: { name: "contacts" },
        },
    ],
    notes: [
        {
            text: "Если вы уверены, что страница должна существовать, сообщите об ошибке в службу поддержки.",
            icon: "fa-solid fa-circle-info",
            tone: "info",
        },
    ],
    visualIcon: "fa-solid fa-map-signs",
    orbitIcon: "fa-solid fa-compass",
    actions: [
        {
            label: "На главную",
            icon: "fa-solid fa-house",
            to: { name: "home" },
            variant: "primary",
        },
        {
            label: "Вернуться назад",
            icon: "fa-solid fa-arrow-left",
            action: "back",
            variant: "secondary",
        },
        {
            label: "Помощь и поддержка",
            icon: "fa-solid fa-circle-question",
            to: { name: "contacts" },
            variant: "info",
        },
    ],
    footer: commonFooter,
};
