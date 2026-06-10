import type { OrganizationNavigationItem } from "../types";

export const ORGANIZATIONS_NAVIGATION: OrganizationNavigationItem[] = [
    {
        key: "organizations",
        label: "Организации",
        hint: "Карточки образовательных организаций",
        routeName: "admin-organizations",
        icon: "building-2",
    },
    {
        key: "departments",
        label: "Отделения",
        hint: "Подразделения организаций",
        routeName: "admin-organization-departments",
        icon: "layers-3",
    },
    {
        key: "studyGroups",
        label: "Группы",
        hint: "Учебные группы и коды вступления",
        routeName: "admin-organization-study-groups",
        icon: "users-round",
    },
    {
        key: "subjects",
        label: "Предметы",
        hint: "Справочник дисциплин",
        routeName: "admin-organization-subjects",
        icon: "book-open",
    },
    {
        key: "teacherOrganizations",
        label: "Преподаватели",
        hint: "Связи преподавателей с организациями",
        routeName: "admin-organization-teachers",
        icon: "graduation-cap",
    },
    {
        key: "teacherSubjects",
        label: "Предметы преподавателей",
        hint: "Назначенные дисциплины",
        routeName: "admin-organization-teacher-subjects",
        icon: "library-big",
    },
    {
        key: "groupCurators",
        label: "Кураторы",
        hint: "Кураторы учебных групп",
        routeName: "admin-organization-group-curators",
        icon: "user-check",
    },
    {
        key: "joinRequests",
        label: "Заявки",
        hint: "Заявки на присоединение",
        routeName: "admin-organization-join-requests",
        icon: "inbox",
    },
];
