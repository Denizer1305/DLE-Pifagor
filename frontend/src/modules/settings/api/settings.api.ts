import { httpClient } from "@/services/api/http.client";
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

const SETTINGS_BASE_URL = "/users/settings/me/";

export async function fetchUserSettings(): Promise<UserSettingsDto> {
    const response = await httpClient.get<UserSettingsDto>(SETTINGS_BASE_URL);

    return response.data;
}

export async function updateUserSettings(
    payload: Partial<UserSettingsDto>,
): Promise<UserSettingsDto> {
    const response = await httpClient.patch<UserSettingsDto>(
        SETTINGS_BASE_URL,
        payload,
    );

    return response.data;
}

export async function fetchAppearanceSettings(): Promise<AppearanceSettingsDto> {
    const response = await httpClient.get<AppearanceSettingsDto>(
        `${SETTINGS_BASE_URL}appearance/`,
    );

    return response.data;
}

export async function updateAppearanceSettings(
    payload: Partial<AppearanceSettingsDto>,
): Promise<AppearanceSettingsDto> {
    const response = await httpClient.patch<AppearanceSettingsDto>(
        `${SETTINGS_BASE_URL}appearance/`,
        payload,
    );

    return response.data;
}

export async function fetchNotificationSettings(): Promise<NotificationSettingsDto> {
    const response = await httpClient.get<NotificationSettingsDto>(
        `${SETTINGS_BASE_URL}notifications/`,
    );

    return response.data;
}

export async function updateNotificationSettings(
    payload: Partial<NotificationSettingsDto>,
): Promise<NotificationSettingsDto> {
    const response = await httpClient.patch<NotificationSettingsDto>(
        `${SETTINGS_BASE_URL}notifications/`,
        payload,
    );

    return response.data;
}

export async function fetchPrivacySettings(): Promise<PrivacySettingsDto> {
    const response = await httpClient.get<PrivacySettingsDto>(
        `${SETTINGS_BASE_URL}privacy/`,
    );

    return response.data;
}

export async function updatePrivacySettings(
    payload: Partial<PrivacySettingsDto>,
): Promise<PrivacySettingsDto> {
    const response = await httpClient.patch<PrivacySettingsDto>(
        `${SETTINGS_BASE_URL}privacy/`,
        payload,
    );

    return response.data;
}

export async function fetchRoleSettings(): Promise<RoleSettingsDto> {
    const response = await httpClient.get<RoleSettingsDto>(
        `${SETTINGS_BASE_URL}roles/`,
    );

    return response.data;
}

export async function updateRoleSettings(
    payload: Partial<RoleSettingsDto>,
): Promise<RoleSettingsDto> {
    const response = await httpClient.patch<RoleSettingsDto>(
        `${SETTINGS_BASE_URL}roles/`,
        payload,
    );

    return response.data;
}

export async function fetchSecuritySettings(): Promise<SecuritySettingsDto> {
    const response = await httpClient.get<SecuritySettingsDto>(
        `${SETTINGS_BASE_URL}security/`,
    );

    return response.data;
}

export async function updateSecuritySettings(
    payload: Partial<SecuritySettingsDto>,
): Promise<SecuritySettingsDto> {
    const response = await httpClient.patch<SecuritySettingsDto>(
        `${SETTINGS_BASE_URL}security/`,
        payload,
    );

    return response.data;
}

export async function changePassword(
    payload: ChangePasswordPayload,
): Promise<{ detail: string }> {
    const response = await httpClient.post<{ detail: string }>(
        `${SETTINGS_BASE_URL}security/change-password/`,
        payload,
    );

    return response.data;
}

export async function fetchSecuritySessions(): Promise<SecuritySessionsDto> {
    const response = await httpClient.get<SecuritySessionsDto>(
        `${SETTINGS_BASE_URL}security/sessions/`,
    );

    return response.data;
}

export async function logoutAllSecuritySessions(): Promise<{ detail: string }> {
    const response = await httpClient.post<{ detail: string }>(
        `${SETTINGS_BASE_URL}security/sessions/logout-all/`,
        {},
    );

    return response.data;
}

export async function logoutSecuritySession(
    sessionId: string,
): Promise<{ detail: string; session_id: string }> {
    const response = await httpClient.post<{ detail: string; session_id: string }>(
        `${SETTINGS_BASE_URL}security/sessions/${sessionId}/logout/`,
        {},
    );

    return response.data;
}