import type { RouteRecordRaw } from "vue-router";

interface SettingsRouteDefinition {
    pathSuffix: string;
    nameSuffix: string;
    title: string;
    component: NonNullable<RouteRecordRaw["component"]>;
}

interface SettingsRouteScope {
    pathPrefix: string;
    namePrefix: string;
    titleSubject?: string;
    roles?: string[];
}

const settingsRouteDefinitions: SettingsRouteDefinition[] = [
    {
        pathSuffix: "",
        nameSuffix: "",
        title: "Настройки",
        component: () => import("@/modules/settings/pages/SettingsPage.vue"),
    },
    {
        pathSuffix: "/appearance",
        nameSuffix: "-appearance",
        title: "Внешний вид",
        component: () => import("@/modules/settings/pages/AppearanceSettingsPage.vue"),
    },
    {
        pathSuffix: "/notifications",
        nameSuffix: "-notifications",
        title: "Уведомления",
        component: () => import("@/modules/settings/pages/NotificationSettingsPage.vue"),
    },
    {
        pathSuffix: "/privacy",
        nameSuffix: "-privacy",
        title: "Приватность",
        component: () => import("@/modules/settings/pages/PrivacySettingsPage.vue"),
    },
    {
        pathSuffix: "/roles",
        nameSuffix: "-roles",
        title: "Ролевые настройки",
        component: () => import("@/modules/settings/pages/RoleSettingsPage.vue"),
    },
    {
        pathSuffix: "/security",
        nameSuffix: "-security",
        title: "Безопасность",
        component: () => import("@/modules/settings/pages/SecuritySettingsPage.vue"),
    },
];

const settingsRouteScopes: SettingsRouteScope[] = [
    {
        pathPrefix: "",
        namePrefix: "",
    },
    {
        pathPrefix: "/teacher",
        namePrefix: "teacher-",
        titleSubject: "преподавателя",
        roles: ["teacher", "curator", "methodist", "organizer", "mentor"],
    },
    {
        pathPrefix: "/student",
        namePrefix: "student-",
        titleSubject: "студента",
        roles: ["learner", "student"],
    },
    {
        pathPrefix: "/parent",
        namePrefix: "parent-",
        titleSubject: "родителя",
        roles: ["guardian"],
    },
    {
        pathPrefix: "/admin",
        namePrefix: "admin-",
        titleSubject: "администратора",
        roles: [
            "superadmin",
            "platform_admin",
            "admin",
            "director",
            "org_admin",
            "department_head",
        ],
    },
];

function createSettingsRoutes(scope: SettingsRouteScope): RouteRecordRaw[] {
    return settingsRouteDefinitions.map((definition) => ({
        path: `${scope.pathPrefix}/settings${definition.pathSuffix}`,
        name: `${scope.namePrefix}settings${definition.nameSuffix}`,
        component: definition.component,
        meta: {
            requiresAuth: true,
            title: `${definition.title}${scope.titleSubject ? ` ${scope.titleSubject}` : ""} | Пифагор`,
            layout: "dashboard",
            ...(scope.roles ? { roles: scope.roles } : {}),
        },
    }));
}

export const settingsRoutes: RouteRecordRaw[] = settingsRouteScopes.flatMap(
    createSettingsRoutes,
);
