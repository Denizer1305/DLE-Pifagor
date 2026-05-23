import type {
    DashboardHeroContent,
    DashboardMiniPlanItem,
    DashboardNavigationItem,
    DashboardCreateItemModalContent,
    DashboardUserProfile,
} from "@/components/dashboard/types/dashboard.types";
import type {
    StudentDashboardModel,
    StudentDashboardSectionContent,
    StudentDashboardSummary,
} from "@/modules/student/types/student-dashboard.types";

import logo from "@/assets/image/logo/logo.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

const dashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

export const studentCreateModalContent: DashboardCreateItemModalContent = {
    closeOverlayLabel: "Закрыть окно",
    closeButtonLabel: "Закрыть",
    cancelLabel: "Отмена",
    calendar: {
        title: "Создать событие",
        description: "Добавьте учебное событие в календарь.",
        titleLabel: "Название события",
        textLabel: "Описание",
        dateLabel: "Дата",
        eventTypeLabel: "Тема события",
        submitLabel: "Создать событие",
    },
    note: {
        title: "Создать заметку",
        description: "Добавьте личную учебную заметку.",
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

const EMPTY_TEXT = "Данные пока не добавлены";

export function createStudentDashboardModel(
    fullName = "",
    summary?: StudentDashboardSummary,
): StudentDashboardModel {
    const profile = createStudentProfile(fullName, summary);
    const hero = createStudentHero();
    const dayCard = createStudentDayCard(summary);
    const miniPlan = createStudentMiniPlan(summary);

    return {
        shell: createStudentShell(profile),

        hero,
        dayCard,
        miniPlan,
        heroSection: {
            hero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайшее расписание",
            miniPlanIcon: "fas fa-clock",
        },

        calendarContent: createStudentCalendarContent(summary),
        calendarDays: summary?.calendar.days ?? [],
        createModal: studentCreateModalContent,

        notifications: {
            title: "Уведомления",
            createLabel: "Создать уведомление",
            items: summary?.notifications ?? [],
            emptyText: "Уведомлений пока нет.",
            actionLabel: "Посмотреть все уведомления",
            actionTo: {
                name: "student-notifications",
            },
        },

        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            items: summary?.notes ?? [],
            emptyText: "Заметок пока нет.",
            actionLabel: "Открыть все заметки",
            actionTo: {
                name: "student-notes",
            },
        },

        profilePanel: {
            user: {
                ...profile,
                avatarAlt: profile.avatarAlt || "Профиль студента",
                roleLabel: profile.roleLabel || "Студент",
            },
            title: "Профиль студента",
            subtitle: "Учебный профиль и настройки кабинета",
            actions: [
                {
                    label: "Мой профиль",
                    icon: "fas fa-user",
                    to: {
                        name: "student-profile",
                    },
                },
                {
                    label: "Настройки",
                    icon: "fas fa-gear",
                    to: {
                        name: "student-settings",
                    },
                },
                {
                    label: "Выйти",
                    icon: "fas fa-arrow-right-from-bracket",
                    action: "logout",
                },
            ],
        },

        stats: summary?.stats ?? createEmptyStudentStats(),

        scheduleSection: createScheduleSection(),
        schedule: summary?.schedule ?? [],

        assignmentsSection: {
            badge: "Контроль",
            icon: "fas fa-list-check",
            title: "Ближайшие задания",
            text: "Домашние работы, тесты и практические задания.",
            emptyIcon: "fas fa-clipboard-check",
            emptyText: "Задания появятся здесь после назначения преподавателем.",
        },
        assignments: summary?.assignments ?? [],

        coursesSection: {
            badge: "Мои курсы",
            icon: "fas fa-book-open",
            title: "Подключённые дисциплины",
            text: "Курсы, материалы и прогресс обучения.",
            emptyIcon: "fas fa-book-open",
            emptyText: "Курсы появятся после подключения студента к дисциплинам.",
        },
        courses: summary?.courses ?? [],

        activitySection: {
            badge: "Последняя активность",
            icon: "fas fa-wave-square",
            title: "Учебные события",
            text: "Изменения по заданиям, результатам и материалам.",
            emptyIcon: "fas fa-wave-square",
            emptyText: "Активность появится после первых действий в курсах.",
        },
        activityItems: summary?.activityItems ?? [],

        gradesSection: {
            badge: "Успеваемость",
            icon: "fas fa-table-list",
            title: "Последние результаты",
            text: "Оценки и статусы по последним работам.",
            emptyIcon: "fas fa-table-list",
            emptyText: "Оценки появятся здесь после проверки первых работ.",
        },
        gradeRows: summary?.gradeRows ?? [],

        goalsSection: {
            badge: "Личные цели",
            icon: "fas fa-bullseye",
            title: "Фокус недели",
            text: "Ориентиры, которые помогают удерживать учебный темп.",
            emptyIcon: "fas fa-bullseye",
            emptyText: "Цели недели появятся после настройки учебного плана.",
        },
        goals: summary?.goals ?? [],
    };
}

export function createEmptyStudentStats() {
    return [
        {
            key: "courses",
            title: "Активные курсы",
            icon: "fas fa-book-open",
            value: 0,
            text: EMPTY_TEXT,
            progress: 0,
        },
        {
            key: "assignments",
            title: "Задания",
            icon: "fas fa-clipboard-check",
            value: 0,
            text: EMPTY_TEXT,
            progress: 0,
        },
        {
            key: "average_grade",
            title: "Средний балл",
            icon: "fas fa-star",
            value: "—",
            text: EMPTY_TEXT,
            progress: 0,
        },
        {
            key: "progress",
            title: "Прогресс",
            icon: "fas fa-chart-line",
            value: "0%",
            text: EMPTY_TEXT,
            progress: 0,
        },
    ];
}

export function createScheduleSection(): StudentDashboardSectionContent {
    return {
        badge: "План на сегодня",
        icon: "fas fa-clock",
        title: "Ближайшее расписание",
        text: "Занятия, консультации и учебные события на день.",
        emptyIcon: "fas fa-calendar-plus",
        emptyText: "Расписание появится после добавления занятий или учебных событий.",
    };
}

function createStudentHero(): DashboardHeroContent {
    return {
        badges: [
            {
                icon: "fas fa-user-graduate",
                label: "Личный кабинет студента",
            },
            {
                icon: "fas fa-book-open",
                label: "Учебное пространство",
            },
        ],
        title: "Личное пространство студента",
        text:
            "Следите за расписанием, курсами, заданиями, оценками и учебными событиями в одном рабочем пространстве.",
        actions: [
            {
                label: "Открыть курсы",
                icon: "fas fa-book-open",
                routeName: "student-courses",
                variant: "primary",
            },
            {
                label: "Проверить задания",
                icon: "fas fa-list-check",
                routeName: "student-assignments",
                variant: "secondary",
            },
        ],
    };
}

function createStudentDayCard(summary?: StudentDashboardSummary) {
    return {
        badge: "Сегодня",
        icon: "fas fa-calendar-day",
        title: getActualDateLabel(summary?.calendar.selectedDate),
        text: getSelectedCalendarText(summary),
        stats: [
            {
                value: summary?.dayStats.lessons ?? 0,
                label: "занятий",
            },
            {
                value: summary?.dayStats.assignments ?? 0,
                label: "заданий",
            },
            {
                value: summary?.dayStats.notifications ?? 0,
                label: "уведомлений",
            },
        ],
    };
}

function createStudentMiniPlan(
    summary?: StudentDashboardSummary,
): DashboardMiniPlanItem[] {
    return (summary?.schedule ?? []).slice(0, 3).map((item) => {
        return {
            time: item.time,
            title: item.title,
            text: item.text,
        };
    });
}

function createStudentProfile(
    fullName: string,
    summary?: StudentDashboardSummary,
): DashboardUserProfile {
    const studentFullName = summary?.profile.fullName || fullName || "Студент";
    const roleLabel = summary?.profile.roleLabel || "Студент";
    const groupLabel = summary?.profile.groupLabel || "";
    const avatarUrl = summary?.profile.avatarUrl || fallbackAvatar;

    return {
        fullName: studentFullName,
        roleLabel: groupLabel
            ? `${roleLabel} · ${groupLabel}`
            : roleLabel,
        avatarUrl,
        avatarAlt: `Профиль студента ${studentFullName}`,
    };
}

function createStudentShell(profile: DashboardUserProfile) {
    return {
        pageClass: "student-dashboard-page",
        role: "student" as const,
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет студента",
        },
        profile: {
            ...profile,
            avatarAlt: profile.avatarAlt || "Профиль студента",
            roleLabel: profile.roleLabel || "Студент",
        },
        navigation: createStudentNavigation(),
        sidebarExtra: {
            variant: "student" as const,
            icon: "fas fa-trophy",
            title: "Учебный прогресс",
            subtitle: "Появится после первых занятий",
            text:
                "Когда backend вернёт курсы, задания и оценки, здесь появится краткая сводка по прогрессу.",
            action: {
                label: "Смотреть прогресс",
                icon: "fas fa-chart-line",
                to: {
                    name: "student-progress",
                },
            },
        },
        search: {
            placeholder: "Поиск по курсам, урокам, заданиям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            ...profile,
            avatarAlt: profile.avatarAlt || "Профиль студента",
            roleLabel: profile.roleLabel || "Студент",
        },
    };
}

function createStudentNavigation(): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Обзор дня и учебная активность",
            icon: "fas fa-house",
            to: {
                name: "student-dashboard",
            },
            exact: true,
        },
        {
            key: "courses",
            label: "Мои курсы",
            description: "Все подключённые дисциплины",
            icon: "fas fa-book-open",
            to: {
                name: "student-courses",
            },
        },
        {
            key: "lessons",
            label: "Уроки",
            description: "Занятия, материалы и темы",
            icon: "fas fa-chalkboard",
            to: {
                name: "student-lessons",
            },
        },
        {
            key: "assignments",
            label: "Задания",
            description: "Домашние, тесты и практика",
            icon: "fas fa-house-laptop",
            to: {
                name: "student-assignments",
            },
        },
        {
            key: "grades",
            label: "Успеваемость",
            description: "Оценки, статусы и результаты",
            icon: "fas fa-table-list",
            to: {
                name: "student-grades",
            },
        },
        {
            key: "progress",
            label: "Прогресс",
            description: "Личный рост и динамика",
            icon: "fas fa-chart-line",
            to: {
                name: "student-progress",
            },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Профиль и параметры кабинета",
            icon: "fas fa-gear",
            to: {
                name: "student-settings",
            },
        },
    ];
}

function createStudentCalendarContent(summary?: StudentDashboardSummary) {
    return {
        title: "Календарь студента",
        monthLabel: summary?.calendar.monthLabel || getMonthLabel(new Date()),
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
                key: "lesson" as const,
                label: "Занятие",
            },
            {
                key: "checking" as const,
                label: "Сдача",
            },
            {
                key: "deadline" as const,
                label: "Дедлайн",
            },
        ],
        noteBadge: "Событие дня",
        createLabel: "Добавить событие",
        fullCalendarLabel: "Открыть полный календарь",
        fullCalendarTo: {
            name: "student-calendar",
        },
    };
}

function getActualDateLabel(value?: string): string {
    const date = parseDateKey(value) || new Date();

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(date);
}

function getSelectedCalendarText(summary?: StudentDashboardSummary): string {
    const selectedDate = summary?.calendar.selectedDate;

    if (!summary || !selectedDate) {
        return "Когда появятся занятия, задания или события на сегодня, они отобразятся здесь.";
    }

    const selectedDay = summary.calendar.days.find((day) => {
        return day.date === selectedDate || day.isSelected;
    });

    if (selectedDay?.text) {
        return selectedDay.text;
    }

    return "Когда появятся занятия, задания или события на выбранный день, они отобразятся здесь.";
}

function getMonthLabel(date: Date): string {
    return new Intl.DateTimeFormat("ru-RU", {
        month: "long",
        year: "numeric",
    }).format(date);
}

function parseDateKey(value?: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);

    if (!year || !month || !day) {
        return null;
    }

    return new Date(year, month - 1, day);
}
