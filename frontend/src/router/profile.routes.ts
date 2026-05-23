import type { RouteRecordRaw } from "vue-router";

export const profileRoutes: RouteRecordRaw[] = [
    {
        path: "/profile",
        name: "profile",
        component: () => import("@/modules/profile/pages/ProfilePage.vue"),
        meta: {
            requiresAuth: true,
            title: "Мой профиль | Пифагор",
            layout: "dashboard",
        },
    },
    {
        path: "/profile/edit",
        name: "profile-edit",
        component: () => import("@/modules/profile/pages/ProfileEditPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Редактирование профиля | Пифагор",
            layout: "dashboard",
        },
    },
    {
        path: "/profile/achievements",
        name: "profile-achievements",
        component: () => import("@/modules/profile/pages/ProfileAchievementsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Достижения и награды | Пифагор",
            layout: "dashboard",
        },
    },

    // -------------------------------------------------------------------------
    // Teacher aliases
    // -------------------------------------------------------------------------

    {
        path: "/teacher/profile",
        name: "teacher-profile",
        component: () => import("@/modules/profile/pages/ProfilePage.vue"),
        meta: {
            requiresAuth: true,
            title: "Профиль преподавателя | Пифагор",
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
    {
        path: "/teacher/profile/edit",
        name: "teacher-profile-edit",
        component: () => import("@/modules/profile/pages/ProfileEditPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Редактирование профиля преподавателя | Пифагор",
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
    {
        path: "/teacher/achievements",
        name: "teacher-achievements",
        component: () => import("@/modules/profile/pages/ProfileAchievementsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Достижения преподавателя | Пифагор",
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

    // -------------------------------------------------------------------------
    // Student aliases
    // -------------------------------------------------------------------------

    {
        path: "/student/profile",
        name: "student-profile",
        component: () => import("@/modules/profile/pages/ProfilePage.vue"),
        meta: {
            requiresAuth: true,
            title: "Профиль студента | Пифагор",
            layout: "dashboard",
            roles: [
                "learner",
                "student",
            ],
        },
    },
    {
        path: "/student/profile/edit",
        name: "student-profile-edit",
        component: () => import("@/modules/profile/pages/ProfileEditPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Редактирование профиля студента | Пифагор",
            layout: "dashboard",
            roles: [
                "learner",
                "student",
            ],
        },
    },
    {
        path: "/student/achievements",
        name: "student-achievements",
        component: () => import("@/modules/profile/pages/ProfileAchievementsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Достижения студента | Пифагор",
            layout: "dashboard",
            roles: [
                "learner",
                "student",
            ],
        },
    },

    // -------------------------------------------------------------------------
    // Admin aliases
    // -------------------------------------------------------------------------

    {
        path: "/admin/profile",
        name: "admin-profile",
        component: () => import("@/modules/profile/pages/ProfilePage.vue"),
        meta: {
            requiresAuth: true,
            title: "Профиль администратора | Пифагор",
            layout: "dashboard",
            roles: [
                "superadmin",
                "director",
                "org_admin",
                "department_head",
            ],
        },
    },
    {
        path: "/admin/profile/edit",
        name: "admin-profile-edit",
        component: () => import("@/modules/profile/pages/ProfileEditPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Редактирование профиля администратора | Пифагор",
            layout: "dashboard",
            roles: [
                "superadmin",
                "director",
                "org_admin",
                "department_head",
            ],
        },
    },
    {
        path: "/admin/achievements",
        name: "admin-achievements",
        component: () => import("@/modules/profile/pages/ProfileAchievementsPage.vue"),
        meta: {
            requiresAuth: true,
            title: "Достижения администратора | Пифагор",
            layout: "dashboard",
            roles: [
                "superadmin",
                "director",
                "org_admin",
                "department_head",
            ],
        },
    },
];
