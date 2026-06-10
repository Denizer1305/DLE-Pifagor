import type { RouteRecordRaw } from "vue-router";

const adminRoles = [
    "superadmin",
    "platform_admin",
    "admin",
];

function createAdminMeta(title: string) {
    return {
        requiresAuth: true,
        roles: adminRoles,
        title,
    };
}

export const adminOrganizationRoutes: RouteRecordRaw[] = [
    {
        path: "/admin/organizations",
        component: () => import("@/modules/organizations/pages/OrganizationAdminPage.vue"),
        redirect: {
            name: "admin-organizations",
        },
        meta: createAdminMeta("Организации | Пифагор"),
        children: [
            {
                path: "",
                name: "admin-organizations",
                component: () => import("@/modules/organizations/pages/OrganizationsPage.vue"),
                meta: createAdminMeta("Организации | Пифагор"),
            },
            {
                path: "departments",
                name: "admin-organization-departments",
                component: () => import("@/modules/organizations/pages/DepartmentsPage.vue"),
                meta: createAdminMeta("Отделения | Пифагор"),
            },
            {
                path: "groups",
                name: "admin-organization-study-groups",
                component: () => import("@/modules/organizations/pages/StudyGroupsPage.vue"),
                meta: createAdminMeta("Учебные группы | Пифагор"),
            },
            {
                path: "subjects",
                name: "admin-organization-subjects",
                component: () => import("@/modules/organizations/pages/SubjectsPage.vue"),
                meta: createAdminMeta("Предметы | Пифагор"),
            },
            {
                path: "teachers",
                name: "admin-organization-teachers",
                component: () => import("@/modules/organizations/pages/TeacherOrganizationsPage.vue"),
                meta: createAdminMeta("Преподаватели организаций | Пифагор"),
            },
            {
                path: "teacher-subjects",
                name: "admin-organization-teacher-subjects",
                component: () => import("@/modules/organizations/pages/TeacherSubjectsPage.vue"),
                meta: createAdminMeta("Предметы преподавателей | Пифагор"),
            },
            {
                path: "group-curators",
                name: "admin-organization-group-curators",
                component: () => import("@/modules/organizations/pages/GroupCuratorsPage.vue"),
                meta: createAdminMeta("Кураторы групп | Пифагор"),
            },
            {
                path: "join-requests",
                name: "admin-organization-join-requests",
                component: () => import("@/modules/organizations/pages/JoinRequestsPage.vue"),
                meta: createAdminMeta("Заявки на присоединение | Пифагор"),
            },
        ],
    },
];
