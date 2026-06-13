import {
    getApiErrorMessage,
    mapApiFieldErrors,
} from "./organizations-common.mapper";

export interface OrganizationMappedError {
    message: string;
    fields: Record<string, string>;
}

export function mapOrganizationError(error: unknown): OrganizationMappedError {
    return {
        message: getApiErrorMessage(error),
        fields: mapApiFieldErrors(error),
    };
}
