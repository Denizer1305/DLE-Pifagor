import type { RouteRecordRaw } from "vue-router";

export const publicRoutes: RouteRecordRaw[] = [
    {
        path: "/",
        name: "home",
        component: () => import("@/modules/public/pages/HomePage.vue"),
        meta: {
            title: "Цифровая образовательная среда | Пифагор",
            layout: "public",
        },
    },
    {
        path: "/about",
        name: "about",
        component: () => import("@/modules/public/pages/AboutPage.vue"),
        meta: {
            title: "О платформе | Пифагор",
            layout: "public",
        },
    },
    {
        path: "/teachers",
        name: "teachers",
        component: () => import("@/modules/public/pages/TeachersPage.vue"),
        meta: {
            title: "Преподаватели | Пифагор",
            layout: "public",
        },
    },
    {
        path: "/contacts",
        name: "contacts",
        component: () => import("@/modules/public/pages/ContactsPage.vue"),
        meta: {
            title: "Контакты | Пифагор",
            layout: "public",
        },
    },
];
