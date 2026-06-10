import type {
    DashboardHeroContent,
    DashboardStatsCardContent,
} from "@/components/dashboard/types/dashboard.types";
import { studentEmptyText } from "@/modules/student/data/student-dashboard.data";
import type { StudentDashboardSectionContent } from "@/modules/student/types/student-dashboard.types";

export const studentDashboardHero: DashboardHeroContent = {
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
    text: "Следите за расписанием, курсами, заданиями, оценками и учебными событиями в одном рабочем пространстве.",
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

export const studentScheduleSection: StudentDashboardSectionContent = {
    badge: "План на сегодня",
    icon: "fas fa-clock",
    title: "Ближайшее расписание",
    text: "Занятия, консультации и учебные события на день.",
    emptyIcon: "fas fa-calendar-plus",
    emptyText: "Расписание появится после добавления занятий или учебных событий.",
};

export const studentDashboardSections = {
    assignments: {
        badge: "Контроль",
        icon: "fas fa-list-check",
        title: "Ближайшие задания",
        text: "Домашние работы, тесты и практические задания.",
        emptyIcon: "fas fa-clipboard-check",
        emptyText: "Задания появятся здесь после назначения преподавателем.",
    },
    courses: {
        badge: "Мои курсы",
        icon: "fas fa-book-open",
        title: "Подключённые дисциплины",
        text: "Курсы, материалы и прогресс обучения.",
        emptyIcon: "fas fa-book-open",
        emptyText: "Курсы появятся после подключения студента к дисциплинам.",
    },
    activity: {
        badge: "Последняя активность",
        icon: "fas fa-wave-square",
        title: "Учебные события",
        text: "Изменения по заданиям, результатам и материалам.",
        emptyIcon: "fas fa-wave-square",
        emptyText: "Активность появится после первых действий в курсах.",
    },
    grades: {
        badge: "Успеваемость",
        icon: "fas fa-table-list",
        title: "Последние результаты",
        text: "Оценки и статусы по последним работам.",
        emptyIcon: "fas fa-table-list",
        emptyText: "Оценки появятся здесь после проверки первых работ.",
    },
    goals: {
        badge: "Личные цели",
        icon: "fas fa-bullseye",
        title: "Фокус недели",
        text: "Ориентиры, которые помогают удерживать учебный темп.",
        emptyIcon: "fas fa-bullseye",
        emptyText: "Цели недели появятся после настройки учебного плана.",
    },
} satisfies Record<string, StudentDashboardSectionContent>;

export function createEmptyStudentStats(): DashboardStatsCardContent[] {
    return [
        {
            key: "courses",
            title: "Активные курсы",
            icon: "fas fa-book-open",
            value: 0,
            text: studentEmptyText,
            progress: 0,
        },
        {
            key: "assignments",
            title: "Задания",
            icon: "fas fa-clipboard-check",
            value: 0,
            text: studentEmptyText,
            progress: 0,
        },
        {
            key: "average_grade",
            title: "Средний балл",
            icon: "fas fa-star",
            value: "-",
            text: studentEmptyText,
            progress: 0,
        },
        {
            key: "progress",
            title: "Прогресс",
            icon: "fas fa-chart-line",
            value: "0%",
            text: studentEmptyText,
            progress: 0,
        },
    ];
}
