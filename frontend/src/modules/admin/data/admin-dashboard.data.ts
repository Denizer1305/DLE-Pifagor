import type {
    DashboardAiCardContent,
    DashboardCalendarContent,
    DashboardCreateItemModalContent,
    DashboardDayCardContent,
    DashboardIntroContent,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import type {
    AdminDashboardProfile,
    AdminDashboardStat,
} from "@/modules/admin/types/admin-dashboard.types";

import { createAdminNavigation } from "@/modules/admin/data/admin-navigation.data";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export const adminFallbackAvatar = fallbackAvatar;

const dashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

export const adminCreateModalContent: DashboardCreateItemModalContent = {
    closeOverlayLabel: "Закрыть окно",
    closeButtonLabel: "Закрыть",
    cancelLabel: "Отмена",
    calendar: {
        title: "Создать событие",
        description: "Добавьте событие в календарь администратора.",
        titleLabel: "Название события",
        textLabel: "Описание",
        dateLabel: "Дата",
        eventTypeLabel: "Тема события",
        submitLabel: "Создать событие",
    },
    note: {
        title: "Создать заметку",
        description: "Добавьте административную заметку или задачу.",
        titleLabel: "Заголовок заметки",
        textLabel: "Текст заметки",
        dateLabel: "Дата",
        eventTypeLabel: "",
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

export function createAdminShellConfig(
    profile: AdminDashboardProfile,
    stats: AdminDashboardStat[] = [],
): DashboardShellConfig {
    const fullName = profile.fullName || profile.email || "Администратор";
    const roleLabel = profile.roleLabel || "Полный доступ · Управление платформой";
    const avatarUrl = profile.avatarUrl || adminFallbackAvatar;

    return {
        pageClass: "admin-dashboard-page",
        role: "admin",
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет администратора",
        },
        profile: {
            fullName,
            roleLabel,
            avatarUrl,
            avatarAlt: "Профиль администратора",
        },
        navigation: createAdminNavigation(stats),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "ИИ-помощник администратора",
            text:
                "Поможет анализировать активность платформы, искать аномалии, готовить сводки и быстрее принимать управленческие решения.",
            image: {
                src: anastasiaLogo,
                alt: "Анастасия",
            },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: {
                    name: "admin-dashboard",
                },
            },
        },
        search: {
            placeholder: "Поиск по пользователям, курсам, обращениям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            fullName,
            roleLabel,
            avatarUrl,
            avatarAlt: "Профиль администратора",
        },
    };
}

export function createAdminCalendarContent(monthLabel: string): DashboardCalendarContent {
    return {
        title: "Календарь администратора",
        monthLabel,
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: [
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб",
            "Вс",
        ],
        noteBadge: "Заметка дня",
        createLabel: "Создать событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: {
            name: "admin-dashboard",
        },
    };
}

export function createAdminNotificationsContent(): DashboardNotificationsContent {
    return {
        title: "Уведомления",
        items: [],
        emptyText: "Уведомлений пока нет.",
    };
}

export function createAdminNotesContent(): DashboardNotesContent {
    return {
        title: "Важные заметки",
        createLabel: "Создать заметку",
        items: [],
        emptyText: "Заметок пока нет.",
    };
}

export function createAdminProfilePanelContent(
    profile: AdminDashboardProfile,
): DashboardProfilePanelContent {
    const fullName = profile.fullName || profile.email || "Администратор";
    const roleLabel = profile.roleLabel || "Полный доступ · Управление платформой";

    return {
        user: {
            fullName,
            roleLabel,
            avatarUrl: profile.avatarUrl || adminFallbackAvatar,
            avatarAlt: "Профиль администратора",
        },
        title: "Профиль администратора",
        subtitle: "Управление аккаунтом и настройками платформы",
        actions: [
            {
                label: "Мой профиль",
                icon: "fas fa-user",
                to: {
                    name: "admin-profile",
                },
            },
            {
                label: "Настройки",
                icon: "fas fa-gear",
                to: {
                    name: "admin-settings",
                },
            },
            {
                label: "Выйти",
                icon: "fas fa-right-from-bracket",
                action: "logout",
            },
        ],
    };
}

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
