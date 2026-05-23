import type {
    AdminDashboardFeaturedStatModel,
    AdminDashboardHeroModel,
    AdminDashboardTimelineItemModel,
} from "@/modules/admin/types/admin-dashboard-page.types";

export const adminDashboardPageUi = {
    loadingText: "Загружаем административную сводку...",
    errorTitle: "Не удалось загрузить кабинет",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    progressLabel: "Динамика",
    emptyTitle: "Данные пока не добавлены",
    plan: {
        icon: "fas fa-calendar-check",
        title: "План администратора",
        text: "Ключевые задачи и рабочие события, которые помогают сохранить ритм платформы.",
        emptyText: "Данные пока не добавлены.",
        emptyIcon: "fas fa-calendar-check",
    },
    critical: {
        badge: "Критические точки",
        icon: "fas fa-triangle-exclamation",
        title: "Критические точки",
        text: "Самые важные участки, на которые сейчас стоит обратить внимание в первую очередь.",
        emptyText: "Критические события появятся здесь, когда backend вернет данные.",
        emptyIcon: "fas fa-circle-check",
    },
    participants: {
        badge: "Пользователи",
        icon: "fas fa-users",
        title: "Управление участниками платформы",
    },
    events: {
        badge: "Последняя активность",
        icon: "fas fa-wave-square",
        title: "Последние события",
        text: "Последние действия пользователей и административные события.",
        emptyText: "События появятся здесь после первых действий на платформе.",
        emptyIcon: "fas fa-wave-square",
    },
    overview: {
        badge: "Аналитика",
        icon: "fas fa-table-list",
        title: "Краткий обзор платформы",
        text: "Основные показатели состояния системы на текущий момент.",
        emptyIcon: "fas fa-table-list",
        emptyText: "Обзор платформы появится здесь, когда backend вернет показатели.",
        headers: [
            "Раздел",
            "Состояние",
            "Значение",
            "Статус",
        ],
        analyticsLabel: "Открыть аналитику",
        reportLabel: "Скачать отчет",
    },
} as const;

export const adminDashboardHero: AdminDashboardHeroModel = {
    badges: [
        {
            label: "Главная панель",
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
            routeName: "admin-users-create",
            variant: "primary",
        },
        {
            label: "Создать курс",
            icon: "fas fa-book-open",
            routeName: "admin-courses-create",
            variant: "secondary",
        },
        {
            label: "Открыть обращения",
            icon: "fas fa-envelope-open-text",
            routeName: "admin-feedback",
            variant: "secondary",
        },
        {
            label: "Смотреть аналитику",
            icon: "fas fa-chart-line",
            routeName: "admin-analytics",
            variant: "secondary",
        },
    ],
};

export const adminDashboardFeaturedStat: AdminDashboardFeaturedStatModel = {
    icon: "fas fa-chart-line",
    title: "Общая активность платформы",
    value: 94,
    label: "Процент выполнения ключевых активностей на платформе за текущую неделю",
    progress: 94,
};

export const adminDashboardPlanItems: AdminDashboardTimelineItemModel[] = [
    {
        time: "09:00",
        title: "Разбор обращений",
        text: "Проверить новые входящие заявки и разделить их по приоритетам.",
    },
    {
        time: "11:30",
        title: "Модерация аккаунтов",
        text: "Проверить преподавателей и заявки на присоединение к организации.",
    },
    {
        time: "14:00",
        title: "Контроль системы",
        text: "Посмотреть логи, активность пользователей и критические события.",
    },
    {
        time: "17:00",
        title: "Обновление сводки",
        text: "Собрать отчётность и подготовить задачи на следующий день.",
    },
];
