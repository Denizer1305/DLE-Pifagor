import { createRouter, createWebHistory } from "vue-router";

import { authRoutes } from "@/router/auth.routes";
import { publicRoutes } from "@/router/public.routes";

const routes = [
    ...publicRoutes,
    ...authRoutes,
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

export default router;
