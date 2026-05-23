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
        path: "/student/profile",
        name: "student-profile",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Профиль студента | Пифагор",
        },
    },
    {
        path: "/student/courses",
        name: "student-courses",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Курсы студента | Пифагор",
        },
    },
    {
        path: "/student/lessons",
        name: "student-lessons",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Уроки студента | Пифагор",
        },
    },
    {
        path: "/student/assignments",
        name: "student-assignments",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Задания студента | Пифагор",
        },
    },
    {
        path: "/student/grades",
        name: "student-grades",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Успеваемость студента | Пифагор",
        },
    },
    {
        path: "/student/progress",
        name: "student-progress",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Прогресс студента | Пифагор",
        },
    },
    {
        path: "/student/calendar",
        name: "student-calendar",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Календарь студента | Пифагор",
        },
    },
    {
        path: "/student/notifications",
        name: "student-notifications",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Уведомления студента | Пифагор",
        },
    },
    {
        path: "/student/notes",
        name: "student-notes",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Заметки студента | Пифагор",
        },
    },
    {
        path: "/student/settings",
        name: "student-settings",
        component: () => import("@/modules/student/pages/StudentPlaceholderPage.vue"),
        meta: {
            ...studentMeta,
            title: "Настройки студента | Пифагор",
        },
    },
];
