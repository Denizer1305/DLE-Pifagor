import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    CodeSetPayload,
    OrganizationDto,
    OrganizationId,
    OrganizationListQuery,
    OrganizationWritePayload,
    TeacherRegistrationCodeResponse,
} from "../types";

const ORGANIZATIONS_URL = "/organizations/admin/organizations/";

function getOrganizationUrl(id: OrganizationId): string {
    return `${ORGANIZATIONS_URL}${id}/`;
}

export function getOrganizations(
    query?: OrganizationListQuery,
) {
    return getApiList<OrganizationDto>(ORGANIZATIONS_URL, query);
}

export function getOrganization(
    id: OrganizationId,
) {
    return getApiDetail<OrganizationDto>(getOrganizationUrl(id));
}

export function createOrganization(
    payload: OrganizationWritePayload,
) {
    return postApi<OrganizationDto, OrganizationWritePayload>(
        ORGANIZATIONS_URL,
        payload,
    );
}

export function updateOrganization(
    id: OrganizationId,
    payload: OrganizationWritePayload,
) {
    return patchApi<OrganizationDto, OrganizationWritePayload>(
        getOrganizationUrl(id),
        payload,
    );
}

export function deactivateOrganization(
    id: OrganizationId,
) {
    return deleteApi<OrganizationDto>(getOrganizationUrl(id));
}

export function restoreOrganization(
    id: OrganizationId,
) {
    return postApi<OrganizationDto>(
        `${getOrganizationUrl(id)}restore/`,
    );
}

export function setTeacherRegistrationCode(
    id: OrganizationId,
    payload: CodeSetPayload,
) {
    return postApi<TeacherRegistrationCodeResponse, CodeSetPayload>(
        `${getOrganizationUrl(id)}teacher-registration-code/`,
        payload,
    );
}

export function disableTeacherRegistrationCode(
    id: OrganizationId,
) {
    return postApi<OrganizationDto>(
        `${getOrganizationUrl(id)}disable-teacher-registration-code/`,
    );
}

export function clearTeacherRegistrationCode(
    id: OrganizationId,
) {
    return postApi<OrganizationDto>(
        `${getOrganizationUrl(id)}clear-teacher-registration-code/`,
    );
}
