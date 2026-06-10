import type { RouteRecordRaw } from "vue-router";

import { authGuard, guestGuard } from "@/router/guards";

export const authRoutes: RouteRecordRaw[] = [
    {
        path: "/login",
        name: "login",
        component: () => import("@/modules/auth/pages/LoginPage.vue"),
        beforeEnter: guestGuard,
        meta: {
            title: "Вход в личный кабинет | Пифагор",
            layout: "auth",
            guestOnly: true,
        },
    },
    {
        path: "/register",
        name: "register",
        component: () => import("@/modules/auth/pages/RegisterPage.vue"),
        beforeEnter: guestGuard,
        meta: {
            title: "Регистрация на платформе | Пифагор",
            layout: "auth",
            guestOnly: true,
        },
    },
    {
        path: "/register/teacher-organization",
        name: "teacher-organization-code",
        component: () => import("@/modules/auth/pages/TeacherOrganizationCodePage.vue"),
        beforeEnter: guestGuard,
        meta: {
            title: "Код организации | Пифагор",
            layout: "auth",
            guestOnly: true,
        },
    },
    {
        path: "/forgot-password",
        name: "forgot-password",
        component: () => import("@/modules/auth/pages/ForgotPasswordPage.vue"),
        beforeEnter: guestGuard,
        meta: {
            title: "Восстановление пароля | Пифагор",
            layout: "auth",
            guestOnly: true,
        },
    },
    {
        path: "/reset-password",
        alias: "/auth/reset-password",
        name: "reset-password",
        component: () => import("@/modules/auth/pages/ResetPasswordPage.vue"),
        beforeEnter: guestGuard,
        meta: {
            title: "Сброс пароля | Пифагор",
            layout: "auth",
            guestOnly: true,
        },
    },
    {
        path: "/verify-email",
        alias: "/auth/verify-email",
        name: "verify-email",
        component: () => import("@/modules/auth/pages/VerifyEmailPage.vue"),
        beforeEnter: guestGuard,
        meta: {
            title: "Подтверждение email | Пифагор",
            layout: "auth",
            guestOnly: true,
        },
    },
    {
        path: "/logout",
        name: "logout",
        component: () => import("@/modules/auth/pages/LogoutPage.vue"),
        beforeEnter: authGuard,
        meta: {
            title: "Выход из аккаунта | Пифагор",
            layout: "auth",
            requiresAuth: true,
        },
    },
];
