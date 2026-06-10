import type { RoleCode } from "@/app/constants/roles.constants";

export type AdminUserRoleGroup = "" | "students" | "teachers" | "parents";
export type AdminUserStatusAction = "block" | "unblock" | "archive" | "restore";

export interface AdminUserRelatedObjectDto {
    id: number;
    name: string;
}

export interface AdminUserRoleDto {
    id: number;
    role: {
        id: number;
        code: RoleCode;
        label: string;
        description?: string;
    };
    organization_payload: AdminUserRelatedObjectDto | null;
    department_payload: AdminUserRelatedObjectDto | null;
    group_payload: AdminUserRelatedObjectDto | null;
    status: string;
    assigned_at: string;
    revoked_at: string | null;
}

export interface AdminUserListDto {
    id: number;
    email: string;
    phone: string;
    first_name: string;
    last_name: string;
    middle_name: string;
    full_name: string;
    birth_date: string | null;
    status: string;
    is_active: boolean;
    is_staff: boolean;
    is_superuser: boolean;
    is_email_verified: boolean;
    is_phone_verified: boolean;
    is_login_allowed: boolean;
    scheduled_for_deletion_at: string | null;
    anonymized_at: string | null;
    created_at: string;
    updated_at: string;
    active_roles: AdminUserRoleDto[];
    primary_role: AdminUserRoleDto | null;
    role_count: number;
}

export interface AdminUserAuditLogDto {
    id: number;
    action: string;
    message: string;
    ip_address: string;
    created_at: string;
}

export interface AdminUserProfileDto {
    id: number;
    gender: string;
    avatar: string | null;
    about: string;
    city: string;
    timezone: string;
    preferred_contact_method: string;
    show_email: boolean;
    show_phone: boolean;
    email_notifications: boolean;
    push_notifications: boolean;
    social_link_max: string;
    social_link_vk: string;
    avatar_moderation_status: string;
    profile_moderation_status: string;
    moderation_comment: string;
    created_at: string;
    updated_at: string;
}

export interface AdminUserDetailDto extends AdminUserListDto {
    backup_email: string;
    email_verified_at: string | null;
    phone_verified_at: string | null;
    account_managed_by: unknown | null;
    login_available_from: string | null;
    login_activation_requested_at: string | null;
    login_activated_at: string | null;
    profile?: AdminUserProfileDto | null;
    user_roles: AdminUserRoleDto[];
    audit_logs: AdminUserAuditLogDto[];
}

export interface AdminUsersFilters {
    roleGroup: AdminUserRoleGroup;
    search: string;
    status: string;
    ordering: string;
    page: number;
    pageSize: number;
}

export interface AdminUsersPaginatedDto {
    data?: AdminUserListDto[];
    results?: AdminUserListDto[];
    meta?: {
        count?: number;
        next?: string | null;
        previous?: string | null;
    };
    count?: number;
    next?: string | null;
    previous?: string | null;
}

export interface AdminUsersListItem {
    id: number;
    fullName: string;
    email: string;
    phone: string;
    roleLabel: string;
    statusLabel: string;
    statusTone: "success" | "warning" | "danger" | "neutral";
    createdAt: string;
    updatedAt: string;
}

export interface AdminUsersSummaryItem {
    key: string;
    label: string;
    value: string | number;
    icon: string;
}

export interface AdminUsersListModel {
    title: string;
    text: string;
    badge: string;
    emptyTitle: string;
    emptyText: string;
    totalLabel: string;
    items: AdminUsersListItem[];
    summary: AdminUsersSummaryItem[];
    total: number;
    currentPage: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
}

export interface AdminUserDetailField {
    label: string;
    value: string;
}

export interface AdminUserDetailModel {
    id: number;
    title: string;
    subtitle: string;
    statusLabel: string;
    roleLabel: string;
    fields: AdminUserDetailField[];
    profileFields: AdminUserDetailField[];
    roles: AdminUserDetailField[];
    audit: AdminUserDetailField[];
    updatedAt: string;
    expectedUpdatedAt: string;
    canBlock: boolean;
    canUnblock: boolean;
    canRestore: boolean;
}

export interface AdminUserEditForm {
    email: string;
    backupEmail: string;
    phone: string;
    firstName: string;
    lastName: string;
    middleName: string;
    birthDate: string;
    isLoginAllowed: boolean;
    reason: string;
}

export interface AdminUserCreateForm extends AdminUserEditForm {
    password: string;
    roleCode: RoleCode | "";
    sendInvite: boolean;
}

export interface AdminUserCreatePayload {
    email: string;
    backup_email?: string;
    phone: string;
    first_name: string;
    last_name: string;
    middle_name?: string;
    birth_date?: string | null;
    is_login_allowed: boolean;
    password?: string;
    role_code?: RoleCode;
    send_invite?: boolean;
    reason?: string;
}

export interface AdminUserUpdatePayload {
    email?: string;
    backup_email?: string;
    phone?: string;
    first_name?: string;
    last_name?: string;
    middle_name?: string;
    birth_date?: string | null;
    is_login_allowed?: boolean;
    expected_updated_at?: string;
    reason?: string;
}
