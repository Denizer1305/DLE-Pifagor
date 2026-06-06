import { ROLE_LABELS, type RoleCode } from "@/app/constants/roles.constants";
import { getAdminUsersPageCopy } from "@/modules/admin/data/admin-users.data";
import type {
    AdminUserCreateForm,
    AdminUserCreatePayload,
    AdminUserDetailDto,
    AdminUserDetailModel,
    AdminUserEditForm,
    AdminUserListDto,
    AdminUsersPaginatedDto,
    AdminUsersFilters,
    AdminUsersListItem,
    AdminUsersListModel,
    AdminUserUpdatePayload,
} from "@/modules/admin/types/admin-users.types";

export function mapAdminUsersList(
    response: AdminUsersPaginatedDto,
    filters: AdminUsersFilters,
): AdminUsersListModel {
    const copy = getAdminUsersPageCopy(filters.roleGroup);
    const results = getPaginatedItems(response);
    const items = results.map(mapAdminUserListItem);
    const total = response.meta?.count ?? response.count ?? items.length;
    const next = response.meta?.next ?? response.next ?? null;
    const previous = response.meta?.previous ?? response.previous ?? null;
    const totalPages = Math.max(1, Math.ceil(total / filters.pageSize));

    return {
        ...copy,
        emptyTitle: "Данные пока не добавлены",
        emptyText: "Попробуйте изменить фильтр или дождитесь появления пользователей.",
        totalLabel: "Всего записей",
        items,
        summary: [
            { key: "total", label: "Всего", value: total, icon: "fas fa-users" },
            { key: "page", label: "На странице", value: items.length, icon: "fas fa-table-list" },
            { key: "verified", label: "Email подтвержден", value: items.filter((item) => item.statusTone === "success").length, icon: "fas fa-shield-check" },
        ],
        total,
        currentPage: filters.page,
        totalPages,
        hasNext: Boolean(next),
        hasPrevious: Boolean(previous),
    };
}

export function mapAdminUserDetail(dto: AdminUserDetailDto): AdminUserDetailModel {
    const roleLabel = getRoleLabel(dto.primary_role?.role.code, dto.primary_role?.role.label);
    const userRoles = Array.isArray(dto.user_roles)
        ? dto.user_roles
        : (Array.isArray(dto.active_roles) ? dto.active_roles : []);
    const auditLogs = Array.isArray(dto.audit_logs) ? dto.audit_logs : [];

    return {
        id: dto.id,
        title: getUserDisplayName(dto),
        subtitle: dto.email,
        statusLabel: getStatusLabel(dto.status),
        roleLabel,
        fields: [
            { label: "Email", value: dto.email },
            { label: "Резервный email", value: dto.backup_email || "Не указан" },
            { label: "Телефон", value: dto.phone || "Не указан" },
            { label: "Дата рождения", value: formatDate(dto.birth_date) },
            { label: "Email подтвержден", value: dto.is_email_verified ? "Да" : "Нет" },
            { label: "Телефон подтвержден", value: dto.is_phone_verified ? "Да" : "Нет" },
            { label: "Вход разрешен", value: dto.is_login_allowed ? "Да" : "Нет" },
            { label: "Создан", value: formatDateTime(dto.created_at) },
        ],
        profileFields: mapProfileFields(dto),
        roles: userRoles.map((userRole) => ({
            label: getRoleLabel(userRole.role.code, userRole.role.label),
            value: [
                userRole.organization_payload?.name,
                userRole.department_payload?.name,
                userRole.group_payload?.name,
            ].filter(Boolean).join(" · ") || "Без привязки",
        })),
        audit: auditLogs.map((log) => ({
            label: formatDateTime(log.created_at),
            value: log.message || log.action,
        })),
        updatedAt: formatDateTime(dto.updated_at),
        expectedUpdatedAt: dto.updated_at,
        canBlock: dto.status !== "blocked",
        canUnblock: dto.status === "blocked",
        canRestore: dto.status === "archived" || dto.status === "scheduled_for_deletion",
    };
}

function mapProfileFields(dto: AdminUserDetailDto) {
    const profile = dto.profile;

    if (!profile) {
        return [
            { label: "Профиль", value: "Профиль пока не заполнен" },
        ];
    }

    return [
        { label: "Город", value: profile.city || "Не указан" },
        { label: "О себе", value: profile.about || "Не указано" },
        { label: "Пол", value: getGenderLabel(profile.gender) },
        { label: "Часовой пояс", value: profile.timezone || "Не указан" },
        { label: "Предпочтительный способ связи", value: getContactMethodLabel(profile.preferred_contact_method) },
        { label: "Показывать email", value: formatBoolean(profile.show_email) },
        { label: "Показывать телефон", value: formatBoolean(profile.show_phone) },
        { label: "Email-уведомления", value: formatBoolean(profile.email_notifications) },
        { label: "Push-уведомления", value: formatBoolean(profile.push_notifications) },
        { label: "MAX", value: profile.social_link_max || "Не указан" },
        { label: "ВК", value: profile.social_link_vk || "Не указан" },
        { label: "Статус аватара", value: getModerationLabel(profile.avatar_moderation_status) },
        { label: "Статус профиля", value: getModerationLabel(profile.profile_moderation_status) },
        { label: "Комментарий модерации", value: profile.moderation_comment || "Нет" },
    ];
}

export function createAdminUserEditForm(dto: AdminUserDetailDto): AdminUserEditForm {
    return {
        email: dto.email || "",
        backupEmail: dto.backup_email || "",
        phone: dto.phone || "",
        firstName: dto.first_name || "",
        lastName: dto.last_name || "",
        middleName: dto.middle_name || "",
        birthDate: dto.birth_date || "",
        isLoginAllowed: dto.is_login_allowed,
        reason: "",
    };
}

export function createAdminUserCreateForm(): AdminUserCreateForm {
    return {
        email: "",
        backupEmail: "",
        phone: "",
        firstName: "",
        lastName: "",
        middleName: "",
        birthDate: "",
        isLoginAllowed: true,
        reason: "",
        password: "",
        roleCode: "",
        sendInvite: true,
    };
}

export function mapAdminUserEditPayload(
    form: AdminUserEditForm,
    expectedUpdatedAt: string,
): AdminUserUpdatePayload {
    return {
        email: form.email.trim(),
        backup_email: form.backupEmail.trim(),
        phone: form.phone.trim(),
        first_name: form.firstName.trim(),
        last_name: form.lastName.trim(),
        middle_name: form.middleName.trim(),
        birth_date: form.birthDate || null,
        is_login_allowed: form.isLoginAllowed,
        expected_updated_at: expectedUpdatedAt,
        reason: form.reason.trim(),
    };
}

export function mapAdminUserCreatePayload(form: AdminUserCreateForm): AdminUserCreatePayload {
    return {
        email: form.email.trim(),
        backup_email: form.backupEmail.trim() || undefined,
        phone: form.phone.trim(),
        first_name: form.firstName.trim(),
        last_name: form.lastName.trim(),
        middle_name: form.middleName.trim() || undefined,
        birth_date: form.birthDate || null,
        is_login_allowed: form.isLoginAllowed,
        password: form.password.trim() || undefined,
        role_code: form.roleCode || undefined,
        send_invite: form.sendInvite,
        reason: form.reason.trim() || undefined,
    };
}

function mapAdminUserListItem(dto: AdminUserListDto): AdminUsersListItem {
    return {
        id: dto.id,
        fullName: getUserDisplayName(dto),
        email: dto.email,
        phone: dto.phone || "Не указан",
        roleLabel: getRoleLabel(dto.primary_role?.role.code, dto.primary_role?.role.label),
        statusLabel: getStatusLabel(dto.status),
        statusTone: getStatusTone(dto.status, dto.is_active),
        createdAt: formatDate(dto.created_at),
        updatedAt: formatDate(dto.updated_at),
    };
}

function getPaginatedItems(response: AdminUsersPaginatedDto): AdminUserListDto[] {
    if (Array.isArray(response.data)) {
        return response.data;
    }

    if (Array.isArray(response.results)) {
        return response.results;
    }

    return [];
}

function getUserDisplayName(user: Pick<AdminUserListDto, "full_name" | "email">): string {
    return user.full_name?.trim() || user.email;
}

function getRoleLabel(code?: RoleCode, fallback = ""): string {
    return code ? ROLE_LABELS[code] || fallback || code : fallback || "Роль не назначена";
}

function getStatusLabel(status: string): string {
    const labels: Record<string, string> = {
        active: "Активен",
        blocked: "Заблокирован",
        archived: "В архиве",
        scheduled_for_deletion: "К удалению",
        anonymized: "Анонимизирован",
    };

    return labels[status] || status || "Не указан";
}

function getStatusTone(
    status: string,
    isActive: boolean,
): AdminUsersListItem["statusTone"] {
    if (!isActive || status === "blocked") {
        return "danger";
    }

    if (status === "archived" || status === "scheduled_for_deletion") {
        return "warning";
    }

    return status === "active" ? "success" : "neutral";
}

function formatBoolean(value: boolean): string {
    return value ? "Да" : "Нет";
}

function getGenderLabel(value: string): string {
    const labels: Record<string, string> = {
        male: "Мужской",
        female: "Женский",
        not_specified: "Не указан",
    };

    return labels[value] || value || "Не указан";
}

function getContactMethodLabel(value: string): string {
    const labels: Record<string, string> = {
        email: "Email",
        phone: "Телефон",
        vk: "ВК",
        max: "MAX",
    };

    return labels[value] || value || "Не указан";
}

function getModerationLabel(value: string): string {
    const labels: Record<string, string> = {
        not_submitted: "Не отправлен",
        pending: "На проверке",
        approved: "Одобрен",
        rejected: "Отклонен",
    };

    return labels[value] || value || "Не указан";
}

function formatDate(value: string | null): string {
    if (!value) {
        return "Не указано";
    }

    return new Intl.DateTimeFormat("ru-RU", { dateStyle: "medium" }).format(new Date(value));
}

function formatDateTime(value: string | null): string {
    if (!value) {
        return "Не указано";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(new Date(value));
}
