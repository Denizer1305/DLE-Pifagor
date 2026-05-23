import { httpClient } from "@/services/api/http.client";
import type {
    SetActiveRolePayload,
    UserSettings,
    UserSettingsUpdatePayload,
} from "../types/user-settings.types";

const SETTINGS_BASE_URL = "/users/settings";

export async function getCurrentUserSettings(): Promise<UserSettings> {
    const response = await httpClient.get<UserSettings>(`${SETTINGS_BASE_URL}/me/`);

    return response.data;
}

export async function updateUserSettings(
    id: number,
    payload: UserSettingsUpdatePayload,
): Promise<UserSettings> {
    const response = await httpClient.patch<UserSettings>(`${SETTINGS_BASE_URL}/${id}/`, payload);

    return response.data;
}

export async function setActiveRole(payload: SetActiveRolePayload): Promise<UserSettings> {
    const response = await httpClient.post<UserSettings>(
        `${SETTINGS_BASE_URL}/set-active-role/`,
        payload,
    );

    return response.data;
}
