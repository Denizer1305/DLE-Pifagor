import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    TeacherOrganizationDto,
    TeacherOrganizationId,
    TeacherOrganizationListQuery,
    TeacherOrganizationWritePayload,
} from "../types";

const TEACHER_ORGANIZATIONS_URL =
    "/organizations/admin/teacher-organizations/";

function getTeacherOrganizationUrl(id: TeacherOrganizationId): string {
    return `${TEACHER_ORGANIZATIONS_URL}${id}/`;
}

export function getTeacherOrganizations(
    query?: TeacherOrganizationListQuery,
) {
    return getApiList<TeacherOrganizationDto>(
        TEACHER_ORGANIZATIONS_URL,
        query,
    );
}

export function getTeacherOrganization(
    id: TeacherOrganizationId,
) {
    return getApiDetail<TeacherOrganizationDto>(
        getTeacherOrganizationUrl(id),
    );
}

export function createTeacherOrganization(
    payload: TeacherOrganizationWritePayload,
) {
    return postApi<TeacherOrganizationDto, TeacherOrganizationWritePayload>(
        TEACHER_ORGANIZATIONS_URL,
        payload,
    );
}

export function updateTeacherOrganization(
    id: TeacherOrganizationId,
    payload: TeacherOrganizationWritePayload,
) {
    return patchApi<TeacherOrganizationDto, TeacherOrganizationWritePayload>(
        getTeacherOrganizationUrl(id),
        payload,
    );
}

export function deactivateTeacherOrganization(
    id: TeacherOrganizationId,
) {
    return deleteApi<TeacherOrganizationDto>(
        getTeacherOrganizationUrl(id),
    );
}

export function restoreTeacherOrganization(
    id: TeacherOrganizationId,
) {
    return postApi<TeacherOrganizationDto>(
        `${getTeacherOrganizationUrl(id)}restore/`,
    );
}

export function setPrimaryTeacherOrganization(
    id: TeacherOrganizationId,
) {
    return postApi<TeacherOrganizationDto>(
        `${getTeacherOrganizationUrl(id)}set-primary/`,
    );
}