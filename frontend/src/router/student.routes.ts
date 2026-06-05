import type { RouteRecordRaw } from "vue-router";

const studentMeta = {
    requiresAuth: true,
    layout: "dashboard",
    roles: [
        "student",
        "learner",
    ],
};

export const studentRoutes: RouteRecordRaw[] = [
    {
        path: "/student",
        name: "student-dashboard",
        component: () => import("@/modules/student/pages/StudentDashboardPage.vue"),
        meta: {
            ...studentMeta,
            title: "Кабинет студента | Пифагор",
        },
    },
    {
        path: "/student/courses",
        name: "student-courses",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Курсы студента | Пифагор",
        },
    },
    {
        path: "/student/lessons",
        name: "student-lessons",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Уроки студента | Пифагор",
        },
    },
    {
        path: "/student/assignments",
        name: "student-assignments",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Задания студента | Пифагор",
        },
    },
    {
        path: "/student/grades",
        name: "student-grades",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Успеваемость студента | Пифагор",
        },
    },
    {
        path: "/student/progress",
        name: "student-progress",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Прогресс студента | Пифагор",
        },
    },
    {
        path: "/student/feedback",
        name: "student-feedback",
        component: () => import("@/modules/feedback/pages/FeedbackPage.vue"),
        meta: {
            ...studentMeta,
            title: "Обращения студента | Пифагор",
        },
    },
    {
        path: "/student/calendar",
        name: "student-calendar",
        component: () => import("@/modules/calendar/pages/CalendarPage.vue"),
        meta: {
            ...studentMeta,
            title: "Календарь студента | Пифагор",
        },
    },
    {
        path: "/student/notifications",
        name: "student-notifications",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Уведомления студента | Пифагор",
        },
    },
    {
        path: "/student/notes",
        name: "student-notes",
        component: () => import("@/modules/notes/pages/NotesPage.vue"),
        meta: {
            ...studentMeta,
            title: "Заметки студента | Пифагор",
        },
    },
];
