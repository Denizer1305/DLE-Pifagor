import { createRouter, createWebHistory } from "vue-router";

import { authRoutes } from "@/router/auth.routes";
import { publicRoutes } from "@/router/public.routes";
import { authGuard, roleGuard } from "@/router/guards";
import type { RoleCode } from "@/app/constants/roles.constants";

import { adminRoutes } from "./admin.routes";
import { parentRoutes } from "./parent.routes";
import { studentRoutes } from "./student.routes";
import { teacherRoutes } from "./teacher.routes";

import { profileRoutes } from "./profile.routes";

const routes = [
    ...publicRoutes,
    ...authRoutes,
    ...adminRoutes,
    ...parentRoutes,
    ...studentRoutes,
    ...teacherRoutes,
    ...profileRoutes,

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
