import type { RoleCode } from "@/app/constants/roles.constants";

export interface UserSettings {
    id: number;
    language: string;
    timezone: string;
    active_role: RoleCode | "";
    interface_theme: string;
    compact_mode: boolean;
    created_at: string;
    updated_at: string;
}

export interface UserSettingsUpdatePayload {
    language?: string;
    timezone?: string;
    interface_theme?: string;
    compact_mode?: boolean;
}

export interface SetActiveRolePayload {
    role_code: RoleCode;
}
