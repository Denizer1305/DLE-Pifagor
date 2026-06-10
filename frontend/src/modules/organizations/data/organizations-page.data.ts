import type {
    OrganizationEntityKey,
    OrganizationPageHeaderView,
    OrganizationSummaryCardView,
} from "../types";

export const ORGANIZATION_ADMIN_PAGE_HEADER: OrganizationPageHeaderView = {
    eyebrow: "Организации",
    title: "Образовательные организации",
    description:
        "Ведите карточки образовательных организаций, контактные данные, публичность и служебные коды подключения.",
};

export const ORGANIZATION_ENTITY_HEADERS: Record<
    OrganizationEntityKey,
    OrganizationPageHeaderView
> = {
    organizations: {
        eyebrow: "Организации",
        title: "Образовательные организации",
        description:
            "Создание, редактирование, публичность и коды подключения образовательных организаций.",
        primaryActionLabel: "Создать организацию",
    },
    departments: {
        eyebrow: "Учебная структура",
        title: "Отделения",
        description:
            "Управление отделениями внутри образовательных организаций.",
        primaryActionLabel: "Создать отделение",
    },
    studyGroups: {
        eyebrow: "Учебная структура",
        title: "Учебные группы",
        description:
            "Группы, курсы, годы обучения, архивирование и коды вступления учащихся.",
        primaryActionLabel: "Создать группу",
    },
    subjects: {
        eyebrow: "Справочники",
        title: "Учебные предметы",
        description:
            "Глобальный справочник дисциплин, используемый в курсах и назначениях преподавателей.",
        primaryActionLabel: "Создать предмет",
    },
    teacherOrganizations: {
        eyebrow: "Преподаватели",
        title: "Преподаватели организаций",
        description:
            "Управление связями преподавателей с образовательными организациями.",
        primaryActionLabel: "Привязать преподавателя",
    },
    teacherSubjects: {
        eyebrow: "Преподаватели",
        title: "Предметы преподавателей",
        description:
            "Назначайте преподавателям учебные предметы и отмечайте основной предмет.",
        primaryActionLabel: "Назначить предмет",
    },
    groupCurators: {
        eyebrow: "Кураторы",
        title: "Кураторы групп",
        description:
            "Назначение и управление кураторами учебных групп.",
        primaryActionLabel: "Назначить куратора",
    },
    joinRequests: {
        eyebrow: "Заявки",
        title: "Заявки пользователей",
        description:
            "Рассматривайте заявки преподавателей в организацию и учащихся в учебные группы.",
        primaryActionLabel: "Обновить заявки",
    },
};

export const ORGANIZATION_SUMMARY_PLACEHOLDERS: OrganizationSummaryCardView[] = [
    {
        key: "organizations",
        label: "Организации",
        value: "—",
        meta: "Всего организаций в системе",
        icon: "building-2",
        tone: "accent",
    },
];
