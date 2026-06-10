import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    TeacherSubjectDto,
    TeacherSubjectId,
    TeacherSubjectListQuery,
    TeacherSubjectWritePayload,
} from "../types";

const TEACHER_SUBJECTS_URL =
    "/organizations/admin/teacher-subjects/";

function getTeacherSubjectUrl(id: TeacherSubjectId): string {
    return `${TEACHER_SUBJECTS_URL}${id}/`;
}

export function getTeacherSubjects(
    query?: TeacherSubjectListQuery,
) {
    return getApiList<TeacherSubjectDto>(
        TEACHER_SUBJECTS_URL,
        query,
    );
}

export function getTeacherSubject(
    id: TeacherSubjectId,
) {
    return getApiDetail<TeacherSubjectDto>(
        getTeacherSubjectUrl(id),
    );
}

export function createTeacherSubject(
    payload: TeacherSubjectWritePayload,
) {
    return postApi<TeacherSubjectDto, TeacherSubjectWritePayload>(
        TEACHER_SUBJECTS_URL,
        payload,
    );
}

export function updateTeacherSubject(
    id: TeacherSubjectId,
    payload: TeacherSubjectWritePayload,
) {
    return patchApi<TeacherSubjectDto, TeacherSubjectWritePayload>(
        getTeacherSubjectUrl(id),
        payload,
    );
}

export function deactivateTeacherSubject(
    id: TeacherSubjectId,
) {
    return deleteApi<TeacherSubjectDto>(
        getTeacherSubjectUrl(id),
    );
}

export function restoreTeacherSubject(
    id: TeacherSubjectId,
) {
    return postApi<TeacherSubjectDto>(
        `${getTeacherSubjectUrl(id)}restore/`,
    );
}

export function setPrimaryTeacherSubject(
    id: TeacherSubjectId,
) {
    return postApi<TeacherSubjectDto>(
        `${getTeacherSubjectUrl(id)}set-primary/`,
    );
}