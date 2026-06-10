import {
    changePassword,
    fetchAppearanceSettings,
    fetchNotificationSettings,
    fetchPrivacySettings,
    fetchRoleSettings,
    fetchSecuritySessions,
    fetchSecuritySettings,
    fetchUserSettings,
    logoutAllSecuritySessions,
    logoutSecuritySession,
    updateAppearanceSettings,
    updateNotificationSettings,
    updatePrivacySettings,
    updateRoleSettings,
    updateSecuritySettings,
    updateUserSettings,
} from "@/modules/settings/api/settings.api";
import type {
    AppearanceSettingsDto,
    ChangePasswordPayload,
    NotificationSettingsDto,
    PrivacySettingsDto,
    RoleSettingsDto,
    SecuritySessionsDto,
    SecuritySettingsDto,
    UserSettingsDto,
} from "@/modules/settings/types/settings.types";

export function getUserSettings(): Promise<UserSettingsDto> {
    return fetchUserSettings();
}

export function saveUserSettings(
    payload: Partial<UserSettingsDto>,
): Promise<UserSettingsDto> {
    return updateUserSettings(payload);
}

export function getAppearanceSettings(): Promise<AppearanceSettingsDto> {
    return fetchAppearanceSettings();
}

export function saveAppearanceSettings(
    payload: Partial<AppearanceSettingsDto>,
): Promise<AppearanceSettingsDto> {
    return updateAppearanceSettings(payload);
}

export function getNotificationSettings(): Promise<NotificationSettingsDto> {
    return fetchNotificationSettings();
}

export function saveNotificationSettings(
    payload: Partial<NotificationSettingsDto>,
): Promise<NotificationSettingsDto> {
    return updateNotificationSettings(payload);
}

export function getPrivacySettings(): Promise<PrivacySettingsDto> {
    return fetchPrivacySettings();
}

export function savePrivacySettings(
    payload: Partial<PrivacySettingsDto>,
): Promise<PrivacySettingsDto> {
    return updatePrivacySettings(payload);
}

export function getRoleSettings(): Promise<RoleSettingsDto> {
    return fetchRoleSettings();
}

export function saveRoleSettings(
    payload: Partial<RoleSettingsDto>,
): Promise<RoleSettingsDto> {
    return updateRoleSettings(payload);
}

export function getSecuritySettings(): Promise<SecuritySettingsDto> {
    return fetchSecuritySettings();
}

export function saveSecuritySettings(
    payload: Partial<SecuritySettingsDto>,
): Promise<SecuritySettingsDto> {
    return updateSecuritySettings(payload);
}

export function savePassword(
    payload: ChangePasswordPayload,
): Promise<{ detail: string }> {
    return changePassword(payload);
}

export function getSecuritySessions(): Promise<SecuritySessionsDto> {
    return fetchSecuritySessions();
}

export function logoutAllSessions(): Promise<{ detail: string }> {
    return logoutAllSecuritySessions();
}

export function logoutSession(
    sessionId: string,
): Promise<{ detail: string; session_id: string }> {
    return logoutSecuritySession(sessionId);
}
