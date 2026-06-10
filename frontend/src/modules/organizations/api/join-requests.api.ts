import {
    getApiDetail,
    getApiList,
    postApi,
} from "./organizations-http.api";
import type {
    JoinRequestDto,
    JoinRequestId,
    JoinRequestListQuery,
    JoinRequestReviewPayload,
} from "../types";

const JOIN_REQUESTS_URL = "/api/v1/users/join-requests/";

function getJoinRequestUrl(id: JoinRequestId): string {
    return `${JOIN_REQUESTS_URL}${id}/`;
}

export function getJoinRequests(
    query?: JoinRequestListQuery,
) {
    return getApiList<JoinRequestDto>(JOIN_REQUESTS_URL, query);
}

export function getJoinRequest(
    id: JoinRequestId,
) {
    return getApiDetail<JoinRequestDto>(getJoinRequestUrl(id));
}

export function approveJoinRequest(
    id: JoinRequestId,
    payload: JoinRequestReviewPayload,
) {
    return postApi<JoinRequestDto, JoinRequestReviewPayload>(
        `${getJoinRequestUrl(id)}approve/`,
        payload,
    );
}

export function rejectJoinRequest(
    id: JoinRequestId,
    payload: JoinRequestReviewPayload,
) {
    return postApi<JoinRequestDto, JoinRequestReviewPayload>(
        `${getJoinRequestUrl(id)}reject/`,
        payload,
    );
}