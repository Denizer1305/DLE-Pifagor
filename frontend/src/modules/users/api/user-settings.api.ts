import { httpClient } from "@/services/api/http.client";
import type {
    SetActiveRolePayload,
    UserSettings,
} from "../types/user-settings.types";

const USER_ROLE_SETTINGS_URL = "/users/settings/me/roles/";

export async function getCurrentUserSettings(): Promise<UserSettings> {
    const response = await httpClient.get<UserSettings>(USER_ROLE_SETTINGS_URL);

    return response.data;
}

export async function setActiveRole(payload: SetActiveRolePayload): Promise<UserSettings> {
    const response = await httpClient.patch<UserSettings>(
        USER_ROLE_SETTINGS_URL,
        {
            active_role: payload.role_code,
        },
    );

    return response.data;
}
