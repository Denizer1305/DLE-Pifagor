import type {
    DashboardAiCardContent,
    DashboardCalendarContent,
    DashboardCreateItemModalContent,
    DashboardDayCardContent,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import type {
    TeacherDashboardHeroModel,
    TeacherDashboardProfile,
    TeacherDashboardSummary,
} from "@/modules/teacher/types/teacher-dashboard.types";

import { createTeacherNavigation } from "@/modules/teacher/data/teacher-navigation.data";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import teacherAvatar from "@/assets/image/avatars/foto_teachers.webp";

export const teacherFallbackAvatar = teacherAvatar;

const dashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

export const teacherCreateModalContent: DashboardCreateItemModalContent = {
    closeOverlayLabel: "Закрыть окно",
    closeButtonLabel: "Закрыть",
    cancelLabel: "Отмена",
    calendar: {
        title: "Создать событие",
        description: "Добавьте событие в календарь преподавателя.",
        titleLabel: "Название события",
        textLabel: "Описание",
        dateLabel: "Дата",
        eventTypeLabel: "Тема события",
        submitLabel: "Создать событие",
    },
    note: {
        title: "Создать заметку",
        description: "Добавьте заметку или задачу преподавателя.",
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

export const teacherDashboardPageUi = {
    loadingText: "Загружаем кабинет преподавателя...",
    errorTitle: "Не удалось загрузить кабинет",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    progressLabel: "Динамика",
    emptyTitle: "Данные пока не добавлены",
    plan: {
        badge: "Сегодня",
        icon: "fas fa-list-check",
        title: "План дня",
        text: "Главное на сегодня: занятия, проверка ответов, обновление материалов и контроль по группам.",
        emptyText: "План дня появится после добавления занятий, дедлайнов или проверок.",
        emptyIcon: "fas fa-list-check",
    },
    attention: {
        badge: "Требует внимания",
        icon: "fas fa-triangle-exclamation",
        title: "Срочные задачи",
        text: "Небольшой список того, что сейчас желательно не откладывать.",
        emptyText: "Срочные задачи появятся здесь, когда их вернет backend.",
        emptyIcon: "fas fa-circle-check",
    },
    courses: {
        badge: "Мои курсы",
        icon: "fas fa-book-open",
        title: "Рабочие курсы преподавателя",
        text: "Активные дисциплины, черновики и курсы, которые требуют обновления материалов.",
        emptyIcon: "fas fa-book-open",
        emptyText: "Курсы преподавателя появятся здесь после создания или назначения.",
        progressLabel: "Прогресс курса",
        filters: [
            "Все",
            "Активные",
            "Черновики",
            "Архив",
        ],
        meta: {
            modules: "модулей",
            students: "студентов",
        },
        actions: {
            open: "Открыть",
            edit: "Редактировать",
            analytics: "Аналитика",
        },
    },
    activity: {
        badge: "Последняя активность",
        icon: "fas fa-wave-square",
        title: "Действия студентов",
        text: "Последние события по заданиям, тестам и активности в курсах.",
        emptyText: "Активность студентов появится после первых действий в курсах.",
        emptyIcon: "fas fa-wave-square",
    },
    journal: {
        badge: "Журнал",
        icon: "fas fa-table-list",
        title: "Краткий обзор группы",
        text: "Последние оценки и текущая учебная ситуация по выбранной группе.",
        emptyIcon: "fas fa-table-list",
        emptyText: "Журнал заполнится после появления студентов, работ и оценок.",
        headers: [
            "Студент",
            "Последняя работа",
            "Оценка",
            "Статус",
        ],
        openLabel: "Открыть журнал",
        analyticsLabel: "Полная аналитика",
    },
} as const;

export const teacherDashboardHero: TeacherDashboardHeroModel = {
    badges: [
        {
            label: "Доброе утро",
            icon: "fas fa-sun",
        },
        {
            label: "Рабочее пространство",
            icon: "fas fa-book",
        },
        {
            label: "Проверка заданий",
            icon: "fas fa-clipboard-check",
        },
    ],
    title: "Рабочее пространство преподавателя",
    text:
        "Здесь собраны курсы, занятия, задания, аналитика и всё, что помогает вести образовательный процесс спокойно и структурно.",
    actions: [
        {
            label: "Создать урок",
            icon: "fas fa-plus",
            routeName: "teacher-lessons-create",
            variant: "primary",
        },
        {
            label: "Создать тест",
            icon: "fas fa-file-circle-plus",
            routeName: "teacher-tests-create",
            variant: "secondary",
        },
        {
            label: "Выдать домашнее задание",
            icon: "fas fa-house-laptop",
            routeName: "teacher-homework-create",
            variant: "secondary",
        },
        {
            label: "Открыть журнал",
            icon: "fas fa-table-list",
            routeName: "teacher-journal",
            variant: "secondary",
        },
    ],
};

export const teacherAiCardContent: DashboardAiCardContent = {
    image: {
        src: anastasiaLogo,
        alt: "Анастасия ИИ",
    },
    title: "Анастасия",
    subtitle: "Именной ИИ-помощник преподавателя",
    text:
        "Поможет составить урок, придумать тест, подготовить домашнее задание или подсказать, на что обратить внимание в аналитике группы.",
    action: {
        label: "Открыть Анастасию",
        icon: "fas fa-sparkles",
        to: {
            name: "teacher-dashboard",
        },
        variant: "primary",
    },
};

export function createTeacherShellConfig(
    profile: TeacherDashboardProfile,
    summary: TeacherDashboardSummary | null,
): DashboardShellConfig {
    const fullName = profile.fullName || "Преподаватель";
    const roleLabel = profile.roleLabel || "Преподаватель";
    const subjectLabel = profile.subjectLabel || "Учебные дисциплины";
    const avatarUrl = profile.avatarUrl || teacherFallbackAvatar;

    return {
        pageClass: "teacher-dashboard-page",
        role: "teacher",
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет преподавателя",
        },
        profile: {
            fullName,
            roleLabel: `${roleLabel} · ${subjectLabel}`,
            avatarUrl,
            avatarAlt: "Профиль преподавателя",
        },
        navigation: createTeacherNavigation(summary),
        sidebarExtra: {
            variant: "ai",
            title: "Анастасия",
            subtitle: "Помощник преподавателя",
            text:
                "Подскажет, как составить урок, сделать тест, выдать домашнее задание и быстрее проверить работы.",
            image: {
                src: anastasiaLogo,
                alt: "Анастасия",
            },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: {
                    name: "teacher-dashboard",
                },
            },
        },
        search: {
            placeholder: "Поиск по курсам, урокам, заданиям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            fullName,
            roleLabel: createTeacherTopbarCaption(summary),
            avatarUrl,
            avatarAlt: "Профиль преподавателя",
        },
    };
}

export function createTeacherCalendarContent(monthLabel: string): DashboardCalendarContent {
    return {
        title: "Календарь преподавателя",
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
        legend: [
            {
                key: "lesson",
                label: "Урок",
            },
            {
                key: "checking",
                label: "Проверка",
            },
            {
                key: "deadline",
                label: "Дедлайн",
            },
        ],
        noteBadge: "Событие дня",
        createLabel: "Создать событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: {
            name: "teacher-calendar",
        },
    };
}

export function createTeacherNotificationsContent(
    summary: TeacherDashboardSummary,
): DashboardNotificationsContent {
    return {
        title: "Уведомления",
        items: summary.notifications.map((item) => {
            return {
                id: item.id,
                icon: item.icon,
                title: item.title,
                text: item.text,
                isNew: item.is_new,
            };
        }),
        emptyText: "Уведомлений пока нет.",
        actionLabel: "Посмотреть все уведомления",
        actionTo: {
            name: "teacher-notifications",
        },
    };
}

export function createTeacherNotesContent(
    summary: TeacherDashboardSummary,
): DashboardNotesContent {
    return {
        title: "Ближайшие заметки",
        createLabel: "Создать заметку",
        items: summary.notes.map((note) => {
            return {
                id: note.id,
                date: note.date,
                title: note.title,
                text: note.text,
            };
        }),
        emptyText: "Заметок пока нет.",
        actionLabel: "Открыть все заметки",
        actionTo: {
            name: "teacher-notes",
        },
    };
}

export function createTeacherProfilePanelContent(
    profile: TeacherDashboardProfile,
): DashboardProfilePanelContent {
    const fullName = profile.fullName || "Преподаватель";
    const roleLabel = profile.roleLabel || "Преподаватель";

    return {
        user: {
            fullName,
            roleLabel,
            avatarUrl: profile.avatarUrl || teacherFallbackAvatar,
            avatarAlt: "Профиль преподавателя",
        },
        title: "Профиль преподавателя",
        subtitle: profile.subjectLabel || "Учебные дисциплины и настройки",
        actions: [
            {
                label: "Мой профиль",
                icon: "fas fa-user",
                to: {
                    name: "teacher-profile",
                },
            },
            {
                label: "Настройки",
                icon: "fas fa-gear",
                to: {
                    name: "teacher-settings",
                },
            },
            {
                label: "Безопасность",
                icon: "fas fa-shield-alt",
                to: {
                    name: "teacher-security",
                },
            },
            {
                label: "Выйти",
                icon: "fas fa-arrow-right-from-bracket",
                action: "logout",
            },
        ],
    };
}

export function createTeacherDayCard(
    summary: TeacherDashboardSummary,
): DashboardDayCardContent {
    return {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: getActualDateLabel(summary.calendar.selectedDate),
        text:
            "Когда backend вернёт занятия, проверки и события на сегодня, они появятся в этой сводке.",
        stats: [
            {
                value: getStatValue(summary, "lessons_today"),
                label: "занятия",
            },
            {
                value: getStatValue(summary, "checking"),
                label: "работы",
            },
            {
                value: getStatValue(summary, "notifications"),
                label: "уведомлений",
            },
        ],
    };
}

function createTeacherTopbarCaption(summary: TeacherDashboardSummary | null): string {
    if (!summary) {
        return "Рабочее пространство преподавателя";
    }

    return `${getStatValue(summary, "lessons_today")} пары · ${getStatValue(summary, "checking")} работ на проверке`;
}

function getStatValue(
    summary: TeacherDashboardSummary,
    key: string,
): string | number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}

function getActualDateLabel(value: string): string {
    const date = parseDateKey(value) || new Date();

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(date);
}

function parseDateKey(value: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);

    if (!year || !month || !day) {
        return null;
    }

    return new Date(year, month - 1, day);
}
