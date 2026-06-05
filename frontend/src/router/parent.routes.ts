import type { RouteRecordRaw } from "vue-router";

const parentMeta = {
    requiresAuth: true,
    layout: "dashboard",
    roles: [
        "guardian",
    ],
};

export const parentRoutes: RouteRecordRaw[] = [
    {
        path: "/parent",
        name: "parent-dashboard",
        component: () => import("@/modules/parent/pages/ParentDashboardPage.vue"),
        meta: {
            ...parentMeta,
            title: "Кабинет родителя | Пифагор",
        },
    },
    {
        path: "/parent/child",
        name: "parent-child",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Профиль ребенка | Пифагор",
        },
    },
    {
        path: "/parent/grades",
        name: "parent-grades",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Успеваемость ребенка | Пифагор",
        },
    },
    {
        path: "/parent/attendance",
        name: "parent-attendance",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Посещаемость ребенка | Пифагор",
        },
    },
    {
        path: "/parent/assignments",
        name: "parent-assignments",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Домашние задания ребенка | Пифагор",
        },
    },
    {
        path: "/parent/schedule",
        name: "parent-schedule",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Расписание ребенка | Пифагор",
        },
    },
    {
        path: "/parent/progress",
        name: "parent-progress",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Прогресс ребенка | Пифагор",
        },
    },
    {
        path: "/parent/messages",
        name: "parent-messages",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Сообщения родителя | Пифагор",
        },
    },
    {
        path: "/parent/feedback",
        name: "parent-feedback",
        component: () => import("@/modules/feedback/pages/FeedbackPage.vue"),
        meta: {
            ...parentMeta,
            title: "Обращения родителя | Пифагор",
        },
    },
    {
        path: "/parent/calendar",
        name: "parent-calendar",
        component: () => import("@/modules/calendar/pages/CalendarPage.vue"),
        meta: {
            ...parentMeta,
            title: "Календарь ребенка | Пифагор",
        },
    },
    {
        path: "/parent/notifications",
        name: "parent-notifications",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Уведомления родителя | Пифагор",
        },
    },
    {
        path: "/parent/notes",
        name: "parent-notes",
        component: () => import("@/modules/notes/pages/NotesPage.vue"),
        meta: {
            ...parentMeta,
            title: "Заметки родителя | Пифагор",
        },
    },
];
