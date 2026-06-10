import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    GroupCuratorDto,
    GroupCuratorId,
    GroupCuratorListQuery,
    GroupCuratorWritePayload,
} from "../types";

const GROUP_CURATORS_URL = "/organizations/admin/group-curators/";

function getGroupCuratorUrl(id: GroupCuratorId): string {
    return `${GROUP_CURATORS_URL}${id}/`;
}

export function getGroupCurators(
    query?: GroupCuratorListQuery,
) {
    return getApiList<GroupCuratorDto>(GROUP_CURATORS_URL, query);
}

export function getGroupCurator(
    id: GroupCuratorId,
) {
    return getApiDetail<GroupCuratorDto>(getGroupCuratorUrl(id));
}

export function createGroupCurator(
    payload: GroupCuratorWritePayload,
) {
    return postApi<GroupCuratorDto, GroupCuratorWritePayload>(
        GROUP_CURATORS_URL,
        payload,
    );
}

export function updateGroupCurator(
    id: GroupCuratorId,
    payload: GroupCuratorWritePayload,
) {
    return patchApi<GroupCuratorDto, GroupCuratorWritePayload>(
        getGroupCuratorUrl(id),
        payload,
    );
}

export function deactivateGroupCurator(
    id: GroupCuratorId,
) {
    return deleteApi<GroupCuratorDto>(getGroupCuratorUrl(id));
}

export function restoreGroupCurator(
    id: GroupCuratorId,
) {
    return postApi<GroupCuratorDto>(
        `${getGroupCuratorUrl(id)}restore/`,
    );
}

export function setPrimaryGroupCurator(
    id: GroupCuratorId,
) {
    return postApi<GroupCuratorDto>(
        `${getGroupCuratorUrl(id)}set-primary/`,
    );
}