import {
    approveJoinRequest as approveJoinRequestApi,
    getJoinRequest,
    getJoinRequests,
    rejectJoinRequest as rejectJoinRequestApi,
} from "../api";
import {
    mapJoinRequestToDetails,
    mapJoinRequestToListItem,
    mapJoinRequestsToListItems,
} from "../mappers";
import { mapJoinRequestReviewFormToPayload } from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    JoinRequestDto,
    JoinRequestId,
    JoinRequestListItemView,
    JoinRequestListQuery,
    JoinRequestReviewFormModel,
    OrganizationDetailsView,
} from "../types";

export interface JoinRequestDetailServiceResult {
    item: JoinRequestDto;
    viewItem: JoinRequestListItemView;
    details: OrganizationDetailsView;
}

export async function loadJoinRequests(
    query?: JoinRequestListQuery,
) {
    const response = await getJoinRequests(query);

    return createListServiceResult(
        response,
        mapJoinRequestsToListItems,
    );
}

export async function loadJoinRequestDetails(
    id: JoinRequestId,
): Promise<JoinRequestDetailServiceResult> {
    const item = await getJoinRequest(id);

    return createJoinRequestDetailServiceResult(item);
}

export async function approveJoinRequest(
    id: JoinRequestId,
    form: JoinRequestReviewFormModel,
): Promise<JoinRequestDetailServiceResult> {
    const item = await approveJoinRequestApi(
        id,
        mapJoinRequestReviewFormToPayload(form),
    );

    return createJoinRequestDetailServiceResult(item);
}

export async function rejectJoinRequest(
    id: JoinRequestId,
    form: JoinRequestReviewFormModel,
): Promise<JoinRequestDetailServiceResult> {
    const item = await rejectJoinRequestApi(
        id,
        mapJoinRequestReviewFormToPayload(form),
    );

    return createJoinRequestDetailServiceResult(item);
}

function createJoinRequestDetailServiceResult(
    item: JoinRequestDto,
): JoinRequestDetailServiceResult {
    return {
        item,
        viewItem: mapJoinRequestToListItem(item),
        details: mapJoinRequestToDetails(item),
    };
}