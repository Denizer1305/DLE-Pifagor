import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    CodeSetPayload,
    GroupJoinCodeResponse,
    StudyGroupDto,
    StudyGroupId,
    StudyGroupListQuery,
    StudyGroupWritePayload,
} from "../types";

const STUDY_GROUPS_URL = "/organizations/admin/study-groups/";

function getStudyGroupUrl(id: StudyGroupId): string {
    return `${STUDY_GROUPS_URL}${id}/`;
}

export function getStudyGroups(
    query?: StudyGroupListQuery,
) {
    return getApiList<StudyGroupDto>(STUDY_GROUPS_URL, query);
}

export function getStudyGroup(
    id: StudyGroupId,
) {
    return getApiDetail<StudyGroupDto>(getStudyGroupUrl(id));
}

export function createStudyGroup(
    payload: StudyGroupWritePayload,
) {
    return postApi<StudyGroupDto, StudyGroupWritePayload>(
        STUDY_GROUPS_URL,
        payload,
    );
}

export function updateStudyGroup(
    id: StudyGroupId,
    payload: StudyGroupWritePayload,
) {
    return patchApi<StudyGroupDto, StudyGroupWritePayload>(
        getStudyGroupUrl(id),
        payload,
    );
}

export function archiveStudyGroup(
    id: StudyGroupId,
) {
    return deleteApi<StudyGroupDto>(getStudyGroupUrl(id));
}

export function restoreStudyGroup(
    id: StudyGroupId,
) {
    return postApi<StudyGroupDto>(
        `${getStudyGroupUrl(id)}restore/`,
    );
}

export function setGroupJoinCode(
    id: StudyGroupId,
    payload: CodeSetPayload,
) {
    return postApi<GroupJoinCodeResponse, CodeSetPayload>(
        `${getStudyGroupUrl(id)}join-code/`,
        payload,
    );
}

export function disableGroupJoinCode(
    id: StudyGroupId,
) {
    return postApi<StudyGroupDto>(
        `${getStudyGroupUrl(id)}disable-join-code/`,
    );
}

export function clearGroupJoinCode(
    id: StudyGroupId,
) {
    return postApi<StudyGroupDto>(
        `${getStudyGroupUrl(id)}clear-join-code/`,
    );
}
