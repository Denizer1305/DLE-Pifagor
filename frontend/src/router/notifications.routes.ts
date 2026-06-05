import type { RouteRecordRaw } from "vue-router";

export const notificationsRoutes: RouteRecordRaw[] = [
    {
        path: "/notifications",
        name: "notifications",
        component: () => import("@/modules/notifications/pages/NotificationsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Уведомления — ЦОС «Пифагор»",
            layout: "dashboard",
        },
    },

    // ---------------------------------------------------------------------
    // Admin aliases
    // ---------------------------------------------------------------------

    {
        path: "/admin/notifications",
        name: "admin-notifications",
        component: () => import("@/modules/notifications/pages/NotificationsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Уведомления администратора — ЦОС «Пифагор»",
            layout: "dashboard",
            roles: [
                "superadmin",
                "director",
                "org_admin",
                "department_head",
            ],
        },
    },

    // ---------------------------------------------------------------------
    // Teacher aliases
    // ---------------------------------------------------------------------

    {
        path: "/teacher/notifications",
        name: "teacher-notifications",
        component: () => import("@/modules/notifications/pages/NotificationsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Уведомления преподавателя — ЦОС «Пифагор»",
            layout: "dashboard",
            roles: [
                "teacher",
                "curator",
                "methodist",
                "organizer",
                "mentor",
            ],
        },
    },

    // ---------------------------------------------------------------------
    // Student aliases
    // ---------------------------------------------------------------------

    {
        path: "/student/notifications",
        name: "student-notifications",
        component: () => import("@/modules/notifications/pages/NotificationsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Уведомления студента — ЦОС «Пифагор»",
            layout: "dashboard",
            roles: [
                "learner",
                "student",
            ],
        },
    },

    // ---------------------------------------------------------------------
    // Parent / guardian aliases
    // ---------------------------------------------------------------------

    {
        path: "/parent/notifications",
        name: "parent-notifications",
        component: () => import("@/modules/notifications/pages/NotificationsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Уведомления родителя — ЦОС «Пифагор»",
            layout: "dashboard",
            roles: [
                "guardian",
            ],
        },
    },
];
