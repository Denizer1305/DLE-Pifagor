import type {
    DashboardCalendarDay,
    DashboardCreateItemModalContent,
    DashboardHeroContent,
    DashboardMiniPlanItem,
    DashboardNavigationItem,
    DashboardUserProfile,
} from "@/components/dashboard/types/dashboard.types";
import type {
    ParentDashboardModel,
    ParentDashboardSectionContent,
    ParentDashboardSummary,
} from "@/modules/parent/types/parent-dashboard.types";

import logo from "@/assets/image/logo/logo.svg";
import fallbackAvatar from "@/assets/image/avatars/anastasia_qe.webp";

const dashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

export const parentCreateModalContent: DashboardCreateItemModalContent = {
    closeOverlayLabel: "Закрыть окно",
    closeButtonLabel: "Закрыть",
    cancelLabel: "Отмена",
    calendar: {
        title: "Создать событие",
        description: "Добавьте семейное или учебное событие в календарь.",
        titleLabel: "Название события",
        textLabel: "Описание",
        dateLabel: "Дата",
        eventTypeLabel: "Тема события",
        submitLabel: "Создать событие",
    },
    note: {
        title: "Создать заметку",
        description: "Добавьте заметку по обучению ребенка.",
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

const EMPTY_TEXT = "Данные пока не добавлены";

export function createParentDashboardModel(
    fullName = "",
    summary?: ParentDashboardSummary,
): ParentDashboardModel {
    const profile = createParentProfile(fullName);
    const hero = createParentHero();
    const dayCard = createParentDayCard(summary);
    const miniPlan = createParentMiniPlan(summary);

    return {
        shell: createParentShell(profile),

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

        calendarContent: createParentCalendarContent(summary),
        calendarDays: summary?.calendar.days ?? createEmptyMonthCalendarDays(),
        createModal: parentCreateModalContent,

        notifications: {
            title: "Уведомления",
            createLabel: "Создать уведомление",
            items: summary?.notifications ?? [],
            emptyText: "Уведомлений пока нет.",
            actionLabel: "Посмотреть все уведомления",
            actionTo: {
                name: "parent-notifications",
            },
        },

        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            items: summary?.notes ?? [],
            emptyText: "Заметок пока нет.",
            actionLabel: "Открыть все заметки",
            actionTo: {
                name: "parent-notes",
            },
        },

        profilePanel: {
            user: {
                ...profile,
            },
            title: "Профиль родителя",
            subtitle: "Доступ к учебному контролю и настройкам кабинета",
            actions: [
                {
                    label: "Мой профиль",
                    icon: "fas fa-user",
                    to: {
                        name: "parent-profile",
                    },
                },
                {
                    label: "Настройки",
                    icon: "fas fa-gear",
                    to: {
                        name: "parent-settings",
                    },
                },
                {
                    label: "Выйти",
                    icon: "fas fa-arrow-right-from-bracket",
                    action: "logout",
                },
            ],
        },

        stats: summary?.stats ?? createEmptyParentStats(),

        scheduleSection: {
            badge: "Неделя",
            icon: "fas fa-calendar-week",
            title: "Ближайшие события",
            text: "Уроки, контрольные, дедлайны и важные события ребенка.",
            emptyIcon: "fas fa-calendar-week",
            emptyText: "Расписание появится здесь после подключения учебного профиля ребенка.",
        },
        schedule: summary?.schedule ?? [],

        notificationsSection: {
            badge: "Важно",
            icon: "fas fa-inbox",
            title: "Уведомления",
            text: "Важные сигналы по учебе, посещаемости и сообщениям.",
            emptyIcon: "fas fa-inbox",
            emptyText: "Важные уведомления появятся здесь, когда backend вернет события.",
        },
        importantItems: summary?.importantItems ?? [],

        coursesSection: {
            badge: "Предметы",
            icon: "fas fa-book-open",
            title: "Текущие учебные предметы",
            text: "Предметы ребенка, прогресс, оценки и ближайшие учебные задачи.",
            emptyIcon: "fas fa-book-open",
            emptyText: "Предметы появятся здесь после привязки ребенка к учебной группе.",
        },
        courses: summary?.courses ?? [],

        activitySection: {
            badge: "Последняя активность",
            icon: "fas fa-wave-square",
            title: "Недавние события",
            text: "Последние действия ребенка в системе и новые учебные события.",
            emptyIcon: "fas fa-wave-square",
            emptyText: "Активность появится после первых действий в личном кабинете ребенка.",
        },
        activityItems: summary?.activityItems ?? [],

        gradesSection: {
            badge: "Успеваемость",
            icon: "fas fa-table-list",
            title: "Последние результаты",
            text: "Краткий обзор последних работ и текущих оценок.",
            emptyIcon: "fas fa-table-list",
            emptyText: "Оценки появятся здесь после проверки первых работ.",
        },
        gradeRows: summary?.gradeRows ?? [],

        messagesSection: {
            badge: "Сообщения",
            icon: "fas fa-envelope-open-text",
            title: "Последние обращения",
            text: "Недавние сообщения от преподавателей и администрации.",
            emptyIcon: "fas fa-envelope-open-text",
            emptyText: "Сообщения появятся здесь, когда преподаватели или администрация напишут вам.",
        },
        messages: summary?.messages ?? [],
    };
}

function createEmptyParentStats() {
    return [
        {
            key: "children",
            title: "Детей",
            icon: "fas fa-child-reaching",
            value: 0,
            text: EMPTY_TEXT,
            progress: 0,
        },
        {
            key: "average_grade",
            title: "Средний балл",
            icon: "fas fa-chart-line",
            value: "—",
            text: EMPTY_TEXT,
            progress: 0,
        },
        {
            key: "attendance",
            title: "Посещаемость",
            icon: "fas fa-calendar-check",
            value: "0%",
            text: EMPTY_TEXT,
            progress: 0,
        },
        {
            key: "messages",
            title: "Сообщения",
            icon: "fas fa-envelope-open-text",
            value: 0,
            text: EMPTY_TEXT,
            progress: 0,
        },
    ];
}

function createParentHero(): DashboardHeroContent {
    return {
        badges: [
            {
                icon: "fas fa-people-roof",
                label: "Личный кабинет родителя",
            },
            {
                icon: "fas fa-chart-simple",
                label: "Учебный контроль",
            },
        ],
        title: "Центр контроля учебы ребенка",
        text:
            "Следите за успеваемостью, посещаемостью, домашними заданиями и сообщениями преподавателей в одном рабочем пространстве.",
        actions: [
            {
                label: "Открыть прогресс",
                icon: "fas fa-chart-simple",
                routeName: "parent-progress",
                variant: "primary",
            },
            {
                label: "Сообщения",
                icon: "fas fa-message",
                routeName: "parent-messages",
                variant: "secondary",
            },
        ],
    };
}

function createParentDayCard(summary?: ParentDashboardSummary) {
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
                value: summary?.dayStats.messages ?? 0,
                label: "сообщений",
            },
        ],
    };
}

function createParentMiniPlan(
    summary?: ParentDashboardSummary,
): DashboardMiniPlanItem[] {
    return (summary?.schedule ?? []).slice(0, 3).map((item) => {
        return {
            time: item.time,
            title: item.title,
            text: item.text,
        };
    });
}

function createParentProfile(fullName: string): DashboardUserProfile {
    const parentFullName = fullName || "Родитель";

    return {
        fullName: parentFullName,
        roleLabel: "Родитель",
        avatarUrl: fallbackAvatar,
        avatarAlt: `Профиль родителя ${parentFullName}`,
    };
}

function createParentShell(profile: DashboardUserProfile) {
    return {
        pageClass: "parent-dashboard-page",
        role: "parent" as const,
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Личный кабинет родителя",
        },
        profile,
        navigation: createParentNavigation(),
        sidebarExtra: {
            variant: "student" as const,
            icon: "fas fa-child",
            title: "Аккаунт ребенка",
            subtitle: "Быстрый переход к учебному профилю",
            text:
                "После привязки ребенка здесь появится быстрый доступ к его успеваемости, посещаемости и домашним заданиям.",
            action: {
                label: "Открыть профиль ребенка",
                icon: "fas fa-arrow-right",
                to: {
                    name: "parent-child",
                },
            },
        },
        search: {
            placeholder: "Поиск по оценкам, предметам, сообщениям...",
            ariaLabel: "Поиск",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: profile,
    };
}

function createParentNavigation(): DashboardNavigationItem[] {
    return [
        {
            key: "dashboard",
            label: "Главная",
            description: "Сводка по ребенку и важные события",
            icon: "fas fa-house",
            to: {
                name: "parent-dashboard",
            },
            exact: true,
        },
        {
            key: "child",
            label: "Мой ребенок",
            description: "Профиль, группа и основная информация",
            icon: "fas fa-user-graduate",
            to: {
                name: "parent-child",
            },
        },
        {
            key: "grades",
            label: "Успеваемость",
            description: "Оценки, динамика и результаты",
            icon: "fas fa-book-open",
            to: {
                name: "parent-grades",
            },
        },
        {
            key: "attendance",
            label: "Посещаемость",
            description: "Пропуски, присутствие и причины",
            icon: "fas fa-calendar-check",
            to: {
                name: "parent-attendance",
            },
        },
        {
            key: "assignments",
            label: "Домашние задания",
            description: "Что задано и что уже выполнено",
            icon: "fas fa-house-laptop",
            to: {
                name: "parent-assignments",
            },
        },
        {
            key: "schedule",
            label: "Расписание",
            description: "Уроки, занятия и ближайшие события",
            icon: "fas fa-clock",
            to: {
                name: "parent-schedule",
            },
        },
        {
            key: "messages",
            label: "Сообщения",
            description: "Диалог с преподавателями и школой",
            icon: "fas fa-envelope-open-text",
            to: {
                name: "parent-messages",
            },
        },
        {
            key: "settings",
            label: "Настройки",
            description: "Профиль и параметры кабинета",
            icon: "fas fa-gear",
            to: {
                name: "parent-settings",
            },
        },
    ];
}

function createParentCalendarContent(summary?: ParentDashboardSummary) {
    return {
        title: "Календарь ребенка",
        monthLabel: summary?.calendar.monthLabel || getMonthLabel(new Date()),
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: [
            "ПН",
            "ВТ",
            "СР",
            "ЧТ",
            "ПТ",
            "СБ",
            "ВС",
        ],
        legend: [
            {
                key: "lesson" as const,
                label: "Урок",
            },
            {
                key: "checking" as const,
                label: "Проверка",
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
            name: "parent-calendar",
        },
    };
}

function createEmptyMonthCalendarDays(): DashboardCalendarDay[] {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const firstDay = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const mondayOffset = (firstDay.getDay() + 6) % 7;
    const days: DashboardCalendarDay[] = [];

    for (let index = 0; index < mondayOffset; index += 1) {
        const date = new Date(year, month, index - mondayOffset + 1);
        days.push(createCalendarDay(date, true));
    }

    for (let day = 1; day <= daysInMonth; day += 1) {
        days.push(createCalendarDay(new Date(year, month, day), false));
    }

    while (days.length % 7 !== 0) {
        const lastDay = days[days.length - 1];
        const lastDate = parseDateKey(lastDay?.date) || today;
        const date = new Date(lastDate);
        date.setDate(lastDate.getDate() + 1);
        days.push(createCalendarDay(date, true));
    }

    return days;
}

function createCalendarDay(date: Date, isMuted: boolean): DashboardCalendarDay {
    const dateKey = formatDateKey(date);
    const isToday = dateKey === formatDateKey(new Date());

    return {
        date: dateKey,
        day: date.getDate(),
        dateLabel: getActualDateLabel(dateKey),
        isToday,
        isSelected: isToday,
        isMuted,
        isWeekend: date.getDay() === 0 || date.getDay() === 6,
        title: isToday ? "Сегодня" : "Событий нет",
        text: "Данные пока не добавлены.",
        events: [],
    };
}

function getActualDateLabel(value?: string): string {
    const date = parseDateKey(value) || new Date();

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(date);
}

function getSelectedCalendarText(summary?: ParentDashboardSummary): string {
    const selectedDate = summary?.calendar.selectedDate;

    if (!summary || !selectedDate) {
        return "После привязки учебного профиля здесь появятся события на выбранный день.";
    }

    const selectedDay = summary.calendar.days.find((day) => {
        return day.date === selectedDate || day.isSelected;
    });

    return selectedDay?.text || "На выбранный день данных пока нет.";
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

function formatDateKey(date: Date): string {
    return [
        date.getFullYear(),
        String(date.getMonth() + 1).padStart(2, "0"),
        String(date.getDate()).padStart(2, "0"),
    ].join("-");
}
