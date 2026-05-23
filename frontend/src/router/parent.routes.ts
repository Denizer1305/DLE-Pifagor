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
        path: "/parent/profile",
        name: "parent-profile",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Профиль родителя | Пифагор",
        },
    },
    {
        path: "/parent/child",
        name: "parent-child",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Профиль ребенка | Пифагор",
        },
    },
    {
        path: "/parent/grades",
        name: "parent-grades",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Успеваемость ребенка | Пифагор",
        },
    },
    {
        path: "/parent/attendance",
        name: "parent-attendance",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Посещаемость ребенка | Пифагор",
        },
    },
    {
        path: "/parent/assignments",
        name: "parent-assignments",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Домашние задания ребенка | Пифагор",
        },
    },
    {
        path: "/parent/schedule",
        name: "parent-schedule",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Расписание ребенка | Пифагор",
        },
    },
    {
        path: "/parent/progress",
        name: "parent-progress",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Прогресс ребенка | Пифагор",
        },
    },
    {
        path: "/parent/messages",
        name: "parent-messages",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Сообщения родителя | Пифагор",
        },
    },
    {
        path: "/parent/calendar",
        name: "parent-calendar",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Календарь ребенка | Пифагор",
        },
    },
    {
        path: "/parent/notifications",
        name: "parent-notifications",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Уведомления родителя | Пифагор",
        },
    },
    {
        path: "/parent/notes",
        name: "parent-notes",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Заметки родителя | Пифагор",
        },
    },
    {
        path: "/parent/settings",
        name: "parent-settings",
        component: () => import("@/modules/parent/pages/ParentPlaceholderPage.vue"),
        meta: {
            ...parentMeta,
            title: "Настройки родителя | Пифагор",
        },
    },
];
