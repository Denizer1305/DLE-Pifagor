import { createRouter, createWebHistory } from "vue-router";

import type { RoleCode } from "@/app/constants/roles.constants";
import { authRoutes } from "@/router/auth.routes";
import { authGuard, roleGuard } from "@/router/guards";
import { publicRoutes } from "@/router/public.routes";

import { adminRoutes } from "./admin.routes";
import { notificationsRoutes } from "./notifications.routes";
import { parentRoutes } from "./parent.routes";
import { profileRoutes } from "./profile.routes";
import { settingsRoutes } from "./settings.routes";
import { studentRoutes } from "./student.routes";
import { teacherRoutes } from "./teacher.routes";

const routes = [
    ...publicRoutes,
    ...authRoutes,
    ...adminRoutes,
    ...parentRoutes,
    ...studentRoutes,
    ...teacherRoutes,
    ...profileRoutes,
    ...settingsRoutes,
    ...notificationsRoutes,

    {
        path: "/forbidden",
        name: "forbidden",
        component: () => import("@/pages/errors/ForbiddenPage.vue"),
        meta: {
            title: "Доступ ограничен | Пифагор",
        },
    },

    {
        path: "/:pathMatch(.*)*",
        name: "not-found",
        component: () => import("@/pages/errors/NotFoundPage.vue"),
        meta: {
            title: "Страница не найдена | Пифагор",
        },
    },
];

export const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return {
            top: 0,
        };
    },
});

router.beforeEach(async (to) => {
    const roles = Array.isArray(to.meta.roles)
        ? to.meta.roles as RoleCode[]
        : [];

    if (roles.length) {
        return roleGuard(roles)(to);
    }

    if (to.meta.requiresAuth) {
        return authGuard(to);
    }

    return true;
});

export default router;
