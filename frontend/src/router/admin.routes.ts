import type { RouteRecordRaw } from "vue-router";

export const adminRoutes: RouteRecordRaw[] = [
    {
        path: "/admin",
        redirect: {
            name: "admin-dashboard",
        },
    },
    {
        path: "/admin/dashboard",
        name: "admin-dashboard",
        component: () => import("@/modules/admin/pages/AdminDashboardPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Кабинет администратора | Пифагор",
        },
    },
    {
        path: "/admin/users",
        name: "admin-users",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Пользователи | Пифагор",
        },
    },
    {
        path: "/admin/courses",
        name: "admin-courses",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Курсы | Пифагор",
        },
    },
    {
        path: "/admin/structure",
        name: "admin-structure",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Структура | Пифагор",
        },
    },
    {
        path: "/admin/feedback",
        name: "admin-feedback",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Обращения | Пифагор",
        },
    },
    {
        path: "/admin/analytics",
        name: "admin-analytics",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Аналитика | Пифагор",
        },
    },
    {
        path: "/admin/system",
        name: "admin-system",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Система | Пифагор",
        },
    },
    {
        path: "/admin/users/create",
        name: "admin-users-create",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Создание пользователя | Пифагор",
        },
    },
    {
        path: "/admin/join-requests",
        name: "admin-join-requests",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Заявки на присоединение | Пифагор",
        },
    },
    {
        path: "/admin/courses/create",
        name: "admin-courses-create",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Создание курса | Пифагор",
        },
    },
    {
        path: "/admin/settings",
        name: "admin-settings",
        component: () => import("@/modules/admin/pages/AdminPlaceholderPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Настройки администратора | Пифагор",
        },
    },
];
