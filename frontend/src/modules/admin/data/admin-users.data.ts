import type { AdminUserRoleGroup } from "@/modules/admin/types/admin-users.types";
import { ROLE_CODES } from "@/app/constants/roles.constants";
import type { RouteLocationRaw } from "vue-router";

interface AdminUsersNavItem {
    key: string;
    label: string;
    icon: string;
    to: RouteLocationRaw;
    badge?: string | number;
    exact?: boolean;
}

export const adminUsersPageContent = {
    loadingText: "Загружаем пользователей...",
    errorTitle: "Не удалось загрузить пользователей",
    retryLabel: "Повторить",
    searchPlaceholder: "Поиск по ФИО, email или телефону",
    applyLabel: "Применить",
    resetLabel: "Сбросить",
    detailsLabel: "Открыть",
    editLabel: "Редактировать",
    previousLabel: "Назад",
    nextLabel: "Вперед",
    totalLabel: "Всего записей",
    emptyTitle: "Данные пока не добавлены",
    emptyText: "Когда пользователи появятся в системе, они будут отображаться здесь.",
    filters: {
        status: "Статус",
        ordering: "Сортировка",
    },
    pages: {
        all: {
            badge: "Пользователи",
            title: "Управление пользователями",
            text: "Просматривайте аккаунты платформы, проверяйте роли и переходите к управлению профилем.",
        },
        students: {
            badge: "Студенты",
            title: "Студенты платформы",
            text: "Список учащихся, доступных текущему администратору.",
        },
        teachers: {
            badge: "Преподаватели",
            title: "Преподаватели и сотрудники",
            text: "Пользователи с преподавательскими и рабочими ролями.",
        },
        parents: {
            badge: "Родители",
            title: "Родители и представители",
            text: "Связанные родительские аккаунты и законные представители.",
        },
    },
};

export const adminUserDetailContent = {
    loadingText: "Загружаем карточку пользователя...",
    errorTitle: "Не удалось загрузить пользователя",
    backLabel: "К списку",
    editLabel: "Редактировать",
    blockLabel: "Заблокировать",
    unblockLabel: "Разблокировать",
    archiveLabel: "Архивировать",
    restoreLabel: "Восстановить",
    mainTitle: "Основные данные",
    rolesTitle: "Роли и связи",
    auditTitle: "Последние действия",
    emptyAudit: "История действий пока пуста.",
};

export const adminUserEditContent = {
    loadingText: "Готовим форму редактирования...",
    errorTitle: "Не удалось загрузить пользователя",
    backLabel: "К карточке",
    title: "Редактирование пользователя",
    text: "Обновите базовые данные аккаунта. Роли и жизненный цикл управляются отдельными действиями.",
    saveLabel: "Сохранить",
    savingLabel: "Сохраняем...",
    fields: {
        email: "Email",
        backupEmail: "Резервный email",
        phone: "Телефон",
        firstName: "Имя",
        lastName: "Фамилия",
        middleName: "Отчество",
        birthDate: "Дата рождения",
        isLoginAllowed: "Вход разрешен",
        reason: "Причина изменения",
    },
};

export const adminUserCreateContent = {
    title: "Создание пользователя",
    text: "Добавьте базовые данные аккаунта, назначьте первичную роль и настройте доступ ко входу.",
    badge: "Новый аккаунт",
    loadingText: "Готовим форму создания пользователя...",
    errorTitle: "Не удалось создать пользователя",
    backLabel: "Все пользователи",
    submitLabel: "Создать пользователя",
    submittingLabel: "Создаём...",
    successMessage: "Пользователь создан.",
    fields: {
        email: "Email",
        backupEmail: "Резервный email",
        phone: "Телефон",
        firstName: "Имя",
        lastName: "Фамилия",
        middleName: "Отчество",
        birthDate: "Дата рождения",
        password: "Временный пароль",
        roleCode: "Первичная роль",
        isLoginAllowed: "Вход разрешен",
        sendInvite: "Отправить приглашение",
        reason: "Комментарий администратора",
    },
    placeholders: {
        roleCode: "Выберите роль",
        password: "Оставьте пустым, если пароль создаст backend",
        reason: "Например: пользователь добавлен по заявке организации.",
    },
};

export const adminUserCreateRoleOptions = [
    { value: "", label: "Без роли" },
    { value: ROLE_CODES.ADMIN, label: "Администратор" },
    { value: ROLE_CODES.TEACHER, label: "Преподаватель" },
    { value: ROLE_CODES.STUDENT, label: "Студент" },
    { value: ROLE_CODES.GUARDIAN, label: "Родитель" },
] as const;

export const adminUserStatusOptions = [
    { value: "", label: "Все статусы" },
    { value: "active", label: "Активные" },
    { value: "blocked", label: "Заблокированные" },
    { value: "archived", label: "В архиве" },
    { value: "scheduled_for_deletion", label: "К удалению" },
] as const;

export const adminUserOrderingOptions = [
    { value: "last_name", label: "ФИО по возрастанию" },
    { value: "-created_at", label: "Сначала новые" },
    { value: "created_at", label: "Сначала старые" },
    { value: "email", label: "Email" },
] as const;

export const adminUsersNavItems: AdminUsersNavItem[] = [
    {
        key: "all",
        label: "Все пользователи",
        icon: "fas fa-users",
        to: { name: "admin-users" },
        exact: true,
    },
    {
        key: "students",
        label: "Студенты",
        icon: "fas fa-user-graduate",
        to: { name: "admin-students" },
    },
    {
        key: "teachers",
        label: "Преподаватели",
        icon: "fas fa-chalkboard-user",
        to: { name: "admin-teachers" },
    },
    {
        key: "parents",
        label: "Родители",
        icon: "fas fa-people-roof",
        to: { name: "admin-parents" },
    },
];

export const adminUsersNavActions: AdminUsersNavItem[] = [
    {
        key: "create",
        label: "Создать пользователя",
        icon: "fas fa-user-plus",
        to: { name: "admin-users-create" },
    },
];

export function getAdminUsersPageCopy(roleGroup: AdminUserRoleGroup) {
    if (roleGroup === "students") {
        return adminUsersPageContent.pages.students;
    }

    if (roleGroup === "teachers") {
        return adminUsersPageContent.pages.teachers;
    }

    if (roleGroup === "parents") {
        return adminUsersPageContent.pages.parents;
    }

    return adminUsersPageContent.pages.all;
}
