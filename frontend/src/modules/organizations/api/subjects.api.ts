import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    SubjectDto,
    SubjectId,
    SubjectListQuery,
    SubjectWritePayload,
} from "../types";

const SUBJECTS_URL = "/organizations/admin/subjects/";

function getSubjectUrl(id: SubjectId): string {
    return `${SUBJECTS_URL}${id}/`;
}

export function getSubjects(
    query?: SubjectListQuery,
) {
    return getApiList<SubjectDto>(SUBJECTS_URL, query);
}

export function getSubject(
    id: SubjectId,
) {
    return getApiDetail<SubjectDto>(getSubjectUrl(id));
}

export function createSubject(
    payload: SubjectWritePayload,
) {
    return postApi<SubjectDto, SubjectWritePayload>(
        SUBJECTS_URL,
        payload,
    );
}

export function updateSubject(
    id: SubjectId,
    payload: SubjectWritePayload,
) {
    return patchApi<SubjectDto, SubjectWritePayload>(
        getSubjectUrl(id),
        payload,
    );
}

export function deactivateSubject(
    id: SubjectId,
) {
    return deleteApi<SubjectDto>(getSubjectUrl(id));
}

export function restoreSubject(
    id: SubjectId,
) {
    return postApi<SubjectDto>(
        `${getSubjectUrl(id)}restore/`,
    );
}