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
        component: () => import("@/modules/admin/pages/AdminUsersPage.vue"),
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
        path: "/admin/users/students",
        name: "admin-students",
        component: () => import("@/modules/admin/pages/AdminStudentsPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Студенты | Пифагор",
        },
    },
    {
        path: "/admin/users/teachers",
        name: "admin-teachers",
        component: () => import("@/modules/admin/pages/AdminTeachersPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Преподаватели | Пифагор",
        },
    },
    {
        path: "/admin/users/parents",
        name: "admin-parents",
        component: () => import("@/modules/admin/pages/AdminParentsPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Родители | Пифагор",
        },
    },
    {
        path: "/admin/users/:id(\\d+)",
        name: "admin-user-detail",
        component: () => import("@/modules/admin/pages/AdminUserDetailPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Карточка пользователя | Пифагор",
        },
    },
    {
        path: "/admin/users/:id(\\d+)/edit",
        name: "admin-user-edit",
        component: () => import("@/modules/admin/pages/AdminUserEditPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Редактирование пользователя | Пифагор",
        },
    },
    {
        path: "/admin/courses",
        name: "admin-courses",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
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
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
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
        component: () => import("@/modules/admin/pages/AdminFeedbackPage.vue"),
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
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
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
        path: "/admin/calendar",
        name: "admin-calendar",
        component: () => import("@/modules/calendar/pages/CalendarPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Календарь администратора | Пифагор",
        },
    },
    {
        path: "/admin/notes",
        name: "admin-notes",
        component: () => import("@/modules/notes/pages/NotesPage.vue"),
        meta: {
            requiresAuth: true,
            roles: [
                "superadmin",
                "platform_admin",
                "admin",
            ],
            title: "Заметки администратора | Пифагор",
        },
    },
    {
        path: "/admin/system",
        name: "admin-system",
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
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
        component: () => import("@/modules/admin/pages/AdminUserCreatePage.vue"),
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
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
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
        component: () => import("@/components/dashboard/shared/DashboardPlaceholderPage.vue"),
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
];
