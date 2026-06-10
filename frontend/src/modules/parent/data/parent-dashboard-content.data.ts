import type {
    DashboardHeroContent,
    DashboardStatsCardContent,
} from "@/components/dashboard/types/dashboard.types";
import { parentEmptyText } from "@/modules/parent/data/parent-dashboard.data";
import type { ParentDashboardSectionContent } from "@/modules/parent/types/parent-dashboard.types";

export const parentDashboardHero: DashboardHeroContent = {
    badges: [
        { icon: "fas fa-people-roof", label: "Личный кабинет родителя" },
        { icon: "fas fa-chart-simple", label: "Учебный контроль" },
    ],
    title: "Центр контроля учебы ребенка",
    text: "Следите за успеваемостью, посещаемостью, домашними заданиями и сообщениями преподавателей в одном рабочем пространстве.",
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

export const parentDashboardSections = {
    schedule: {
        badge: "Неделя",
        icon: "fas fa-calendar-week",
        title: "Ближайшие события",
        text: "Уроки, контрольные, дедлайны и важные события ребенка.",
        emptyIcon: "fas fa-calendar-week",
        emptyText: "Расписание появится здесь после подключения учебного профиля ребенка.",
    },
    notifications: {
        badge: "Важно",
        icon: "fas fa-inbox",
        title: "Уведомления",
        text: "Важные сигналы по учебе, посещаемости и сообщениям.",
        emptyIcon: "fas fa-inbox",
        emptyText: "Важные уведомления появятся здесь, когда backend вернет события.",
    },
    courses: {
        badge: "Предметы",
        icon: "fas fa-book-open",
        title: "Текущие учебные предметы",
        text: "Предметы ребенка, прогресс, оценки и ближайшие учебные задачи.",
        emptyIcon: "fas fa-book-open",
        emptyText: "Предметы появятся здесь после привязки ребенка к учебной группе.",
    },
    activity: {
        badge: "Последняя активность",
        icon: "fas fa-wave-square",
        title: "Недавние события",
        text: "Последние действия ребенка в системе и новые учебные события.",
        emptyIcon: "fas fa-wave-square",
        emptyText: "Активность появится после первых действий в личном кабинете ребенка.",
    },
    grades: {
        badge: "Успеваемость",
        icon: "fas fa-table-list",
        title: "Последние результаты",
        text: "Краткий обзор последних работ и текущих оценок.",
        emptyIcon: "fas fa-table-list",
        emptyText: "Оценки появятся здесь после проверки первых работ.",
    },
    messages: {
        badge: "Сообщения",
        icon: "fas fa-envelope-open-text",
        title: "Последние обращения",
        text: "Недавние сообщения от преподавателей и администрации.",
        emptyIcon: "fas fa-envelope-open-text",
        emptyText: "Сообщения появятся здесь, когда преподаватели или администрация напишут вам.",
    },
} satisfies Record<string, ParentDashboardSectionContent>;

export function createEmptyParentStats(): DashboardStatsCardContent[] {
    return [
        {
            key: "children",
            title: "Детей",
            icon: "fas fa-child-reaching",
            value: 0,
            text: parentEmptyText,
            progress: 0,
        },
        {
            key: "average_grade",
            title: "Средний балл",
            icon: "fas fa-chart-line",
            value: "-",
            text: parentEmptyText,
            progress: 0,
        },
        {
            key: "attendance",
            title: "Посещаемость",
            icon: "fas fa-calendar-check",
            value: "0%",
            text: parentEmptyText,
            progress: 0,
        },
        {
            key: "messages",
            title: "Сообщения",
            icon: "fas fa-envelope-open-text",
            value: 0,
            text: parentEmptyText,
            progress: 0,
        },
    ];
}
