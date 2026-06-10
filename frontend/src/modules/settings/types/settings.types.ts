import type {
    DashboardCalendarContent,
    DashboardPageScaffoldModel,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";

export type SettingsTheme =
    | "light"
    | "blue"
    | "light-blue"
    | "green"
    | "orange"
    | "pinki"
    | "violet"
    | "red"
    | "yellow"
    | "dark";

export type SettingsColorMode = "light" | "dark" | "system";

export type SettingsDensity = "compact" | "comfortable" | "spacious";

export type SettingsLanguage = "ru" | "en" | "de" | "fr";

export type NotificationFrequency =
    | "instant"
    | "daily"
    | "weekly"
    | "disabled";

export type ProfileVisibility =
    | "public"
    | "organization"
    | "role_only"
    | "private";

export type SessionLifetimeMode =
    | "standard"
    | "extended"
    | "strict";

export type SettingsRoleCode =
    | "teacher"
    | "learner"
    | "guardian"
    | "admin";

export interface AppearanceSettingsDto {
    theme: SettingsTheme;
    color_mode: SettingsColorMode;
    density: SettingsDensity;
    language: SettingsLanguage;
    animations_enabled: boolean;
    glass_panels_enabled: boolean;
    rounded_cards_enabled: boolean;
    sticky_sidebar_enabled: boolean;
    large_cards_enabled: boolean;
}

export interface NotificationSettingsDto {
    channels: {
        in_app: boolean;
        email: boolean;
        vk: boolean;
        max: boolean;
    };
    frequency: {
        security: NotificationFrequency;
        education: NotificationFrequency;
        assignments: NotificationFrequency;
        schedule: NotificationFrequency;
        feedback: NotificationFrequency;
        system: NotificationFrequency;
        digest: NotificationFrequency;
        marketing: NotificationFrequency;
    };
    digest_time: string;
}

export interface PrivacySettingsDto {
    profile_visibility: ProfileVisibility;
    show_email: boolean;
    show_phone: boolean;
    show_city: boolean;
    show_birth_date: boolean;
    show_role_profile: boolean;
    show_achievements: boolean;
    allow_teachers_access: boolean;
    allow_students_access: boolean;
    allow_guardians_access: boolean;
    allow_admins_access: boolean;
    allow_data_export: boolean;
}

export interface SecuritySettingsDto {
    login_notifications_enabled: boolean;
    suspicious_activity_notifications_enabled: boolean;
    trusted_devices_enabled: boolean;
    session_lifetime_mode: SessionLifetimeMode;
    two_factor_enabled: boolean;
}

export interface RoleSettingsDto {
    active_role: SettingsRoleCode;
    roles: {
        teacher: TeacherRoleSettingsDto;
        learner: LearnerRoleSettingsDto;
        guardian: GuardianRoleSettingsDto;
        admin: AdminRoleSettingsDto;
    };
}

export interface TeacherRoleSettingsDto {
    show_hero_block: boolean;
    show_topbar: boolean;
    show_sidebar: boolean;
    show_quick_overview: boolean;
    show_profile_contacts: boolean;
    show_profile_role_section: boolean;
    show_sidebar_ai: boolean;
    show_ai_card: boolean;
    show_lesson_hints: boolean;
    show_group_analytics: boolean;
}

export interface LearnerRoleSettingsDto {
    show_hero_block: boolean;
    show_progress: boolean;
    show_assignments: boolean;
    show_schedule: boolean;
    show_achievements: boolean;
    show_ai_hints: boolean;
}

export interface GuardianRoleSettingsDto {
    show_children_progress: boolean;
    show_teacher_contacts: boolean;
    show_notifications: boolean;
    show_schedule: boolean;
}

export interface AdminRoleSettingsDto {
    show_system_summary: boolean;
    show_moderation_panel: boolean;
    show_audit_events: boolean;
    show_support_requests: boolean;
}

export interface UserSettingsDto {
    appearance: AppearanceSettingsDto;
    notifications: NotificationSettingsDto;
    privacy: PrivacySettingsDto;
    security: SecuritySettingsDto;
    roles: RoleSettingsDto;
}

export interface ChangePasswordPayload {
    current_password: string;
    new_password: string;
    new_password_confirm: string;
}

export interface SecuritySessionDto {
    id: string;
    title: string;
    device: string;
    ip_address: string;
    is_current: boolean;
    last_activity: string;
}

export interface SecuritySessionsDto {
    items: SecuritySessionDto[];
    can_logout_all: boolean;
}

export interface SettingsHeroModel {
    icon: string;
    topline: string;
    title: string;
    text: string;
    badges: {
        icon: string;
        label: string;
    }[];
    summaryRows: {
        label: string;
        value: string | number;
    }[];
}

export interface SettingsCenterCardModel {
    key: string;
    icon: string;
    title: string;
    text: string;
    badge?: string;
    routeName: string;
}

export interface SettingsCenterModel {
    scaffold: DashboardPageScaffoldModel;
    hero: SettingsHeroModel;
    cards: SettingsCenterCardModel[];
}

export interface AppearanceThemeModel {
    key: SettingsTheme;
    title: string;
    text: string;
    previewClass: string;
    tokens: string[];
}

export interface SettingsToggleItemModel {
    key: string;
    label: string;
    text: string;
    value: boolean;
}

export interface SettingsSelectOptionModel {
    value: string;
    label: string;
    text?: string;
}

export interface SettingsPageState<TSettings> {
    scaffold: DashboardPageScaffoldModel;
    hero: SettingsHeroModel;
    settings: TSettings;
}

export interface PasswordFormState {
    currentPassword: string;
    newPassword: string;
    newPasswordConfirm: string;
}

export interface PasswordFormErrors {
    currentPassword: string;
    newPassword: string;
    newPasswordConfirm: string;
    common: string;
}

export interface SettingsPasswordFieldModel {
    key: keyof PasswordFormState;
    label: string;
    text: string;
    autocomplete: string;
}

export interface SettingsPasswordFormContent {
    fields: SettingsPasswordFieldModel[];
    errorIcon: string;
    submitIcon: string;
    submitLabel: string;
    submittingLabel: string;
}
