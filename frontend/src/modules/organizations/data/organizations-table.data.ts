import type {
    OrganizationEntityKey,
    OrganizationTableAction,
    OrganizationTableActionKey,
    OrganizationTableConfig,
} from "../types";

export const ORGANIZATION_TABLE_ACTIONS: Record<OrganizationTableActionKey, OrganizationTableAction> = {
    details: {
        key: "details",
        label: "Подробнее",
        icon: "eye",
        tone: "neutral",
    },
    edit: {
        key: "edit",
        label: "Редактировать",
        icon: "pencil",
        tone: "accent",
    },
    archive: {
        key: "archive",
        label: "В архив",
        icon: "archive",
        tone: "warning",
    },
    deactivate: {
        key: "deactivate",
        label: "Деактивировать",
        icon: "ban",
        tone: "danger",
        isDanger: true,
    },
    restore: {
        key: "restore",
        label: "Восстановить",
        icon: "rotate-ccw",
        tone: "success",
    },
    delete: {
        key: "delete",
        label: "Удалить",
        icon: "trash-2",
        tone: "danger",
        isDanger: true,
    },
    setCode: {
        key: "setCode",
        label: "Установить код",
        icon: "key-round",
        tone: "accent",
    },
    disableCode: {
        key: "disableCode",
        label: "Отключить код",
        icon: "key-square",
        tone: "warning",
    },
    clearCode: {
        key: "clearCode",
        label: "Очистить код",
        icon: "trash-2",
        tone: "danger",
        isDanger: true,
    },
    setPrimary: {
        key: "setPrimary",
        label: "Сделать основным",
        icon: "star",
        tone: "accent",
    },
    approve: {
        key: "approve",
        label: "Принять",
        icon: "check",
        tone: "success",
    },
    reject: {
        key: "reject",
        label: "Отклонить",
        icon: "x",
        tone: "danger",
        isDanger: true,
    },
};

export const ORGANIZATION_TABLE_CONFIGS: Record<
    OrganizationEntityKey,
    OrganizationTableConfig
> = {
    organizations: {
        entity: "organizations",
        columns: [
            {
                key: "entity",
                label: "Организация",
                isSortable: true,
            },
            {
                key: "city",
                label: "Город",
                width: "140px",
            },
            {
                key: "contacts",
                label: "Контакты",
                width: "220px",
                isHiddenOnMobile: true,
            },
            {
                key: "status",
                label: "Статус",
                width: "150px",
            },
            {
                key: "actions",
                label: "",
                width: "160px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.setCode,
            ORGANIZATION_TABLE_ACTIONS.deactivate,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    departments: {
        entity: "departments",
        columns: [
            {
                key: "entity",
                label: "Отделение",
                isSortable: true,
            },
            {
                key: "organization",
                label: "Организация",
                width: "260px",
            },
            {
                key: "status",
                label: "Статус",
                width: "140px",
            },
            {
                key: "actions",
                label: "",
                width: "140px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.deactivate,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    studyGroups: {
        entity: "studyGroups",
        columns: [
            {
                key: "entity",
                label: "Группа",
                isSortable: true,
            },
            {
                key: "department",
                label: "Отделение",
                width: "240px",
            },
            {
                key: "period",
                label: "Период",
                width: "150px",
            },
            {
                key: "status",
                label: "Статус",
                width: "140px",
            },
            {
                key: "actions",
                label: "",
                width: "170px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.setCode,
            ORGANIZATION_TABLE_ACTIONS.archive,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    subjects: {
        entity: "subjects",
        columns: [
            {
                key: "entity",
                label: "Предмет",
                isSortable: true,
            },
            {
                key: "code",
                label: "Код",
                width: "160px",
            },
            {
                key: "status",
                label: "Статус",
                width: "140px",
            },
            {
                key: "actions",
                label: "",
                width: "140px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.deactivate,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    teacherOrganizations: {
        entity: "teacherOrganizations",
        columns: [
            {
                key: "teacher",
                label: "Преподаватель",
                isSortable: true,
            },
            {
                key: "organization",
                label: "Организация",
                width: "260px",
            },
            {
                key: "position",
                label: "Должность",
                width: "220px",
            },
            {
                key: "status",
                label: "Статус",
                width: "150px",
            },
            {
                key: "actions",
                label: "",
                width: "170px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.setPrimary,
            ORGANIZATION_TABLE_ACTIONS.deactivate,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    teacherSubjects: {
        entity: "teacherSubjects",
        columns: [
            {
                key: "teacher",
                label: "Преподаватель",
                isSortable: true,
            },
            {
                key: "subject",
                label: "Предмет",
                width: "240px",
            },
            {
                key: "status",
                label: "Статус",
                width: "150px",
            },
            {
                key: "actions",
                label: "",
                width: "170px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.setPrimary,
            ORGANIZATION_TABLE_ACTIONS.deactivate,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    groupCurators: {
        entity: "groupCurators",
        columns: [
            {
                key: "teacher",
                label: "Куратор",
                isSortable: true,
            },
            {
                key: "group",
                label: "Группа",
                width: "220px",
            },
            {
                key: "status",
                label: "Статус",
                width: "150px",
            },
            {
                key: "actions",
                label: "",
                width: "170px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.edit,
            ORGANIZATION_TABLE_ACTIONS.setPrimary,
            ORGANIZATION_TABLE_ACTIONS.deactivate,
            ORGANIZATION_TABLE_ACTIONS.restore,
        ],
    },
    joinRequests: {
        entity: "joinRequests",
        columns: [
            {
                key: "user",
                label: "Пользователь",
                isSortable: true,
            },
            {
                key: "type",
                label: "Тип заявки",
                width: "220px",
            },
            {
                key: "target",
                label: "Куда",
                width: "260px",
            },
            {
                key: "status",
                label: "Статус",
                width: "150px",
            },
            {
                key: "actions",
                label: "",
                width: "170px",
                align: "right",
            },
        ],
        actions: [
            ORGANIZATION_TABLE_ACTIONS.details,
            ORGANIZATION_TABLE_ACTIONS.approve,
            ORGANIZATION_TABLE_ACTIONS.reject,
        ],
    },
};
