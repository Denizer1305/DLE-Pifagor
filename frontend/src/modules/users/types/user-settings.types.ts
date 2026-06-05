import type { RoleCode } from "@/app/constants/roles.constants";

export interface UserSettings {
    active_role: RoleCode | "";
}

export interface SetActiveRolePayload {
    role_code: RoleCode;
}
