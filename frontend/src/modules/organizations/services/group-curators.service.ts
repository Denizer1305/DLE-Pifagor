import {
    createGroupCurator as createGroupCuratorApi,
    deactivateGroupCurator,
    getGroupCurator,
    getGroupCurators,
    restoreGroupCurator,
    setPrimaryGroupCurator,
    updateGroupCurator as updateGroupCuratorApi,
} from "../api";
import {
    mapGroupCuratorToDetails,
    mapGroupCuratorToListItem,
    mapGroupCuratorsToListItems,
} from "../mappers";
import { mapGroupCuratorFormToPayload } from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    GroupCuratorDto,
    GroupCuratorFormModel,
    GroupCuratorId,
    GroupCuratorListItemView,
    GroupCuratorListQuery,
    OrganizationDetailsView,
} from "../types";

export interface GroupCuratorDetailServiceResult {
    item: GroupCuratorDto;
    viewItem: GroupCuratorListItemView;
    details: OrganizationDetailsView;
}

export async function loadGroupCurators(
    query?: GroupCuratorListQuery,
) {
    const response = await getGroupCurators(query);

    return createListServiceResult(
        response,
        mapGroupCuratorsToListItems,
    );
}

export async function loadGroupCuratorDetails(
    id: GroupCuratorId,
): Promise<GroupCuratorDetailServiceResult> {
    const item = await getGroupCurator(id);

    return createGroupCuratorDetailServiceResult(item);
}

export async function createGroupCurator(
    form: GroupCuratorFormModel,
): Promise<GroupCuratorDetailServiceResult> {
    const item = await createGroupCuratorApi(
        mapGroupCuratorFormToPayload(form),
    );

    return createGroupCuratorDetailServiceResult(item);
}

export async function updateGroupCurator(
    id: GroupCuratorId,
    form: GroupCuratorFormModel,
): Promise<GroupCuratorDetailServiceResult> {
    const item = await updateGroupCuratorApi(
        id,
        mapGroupCuratorFormToPayload(form),
    );

    return createGroupCuratorDetailServiceResult(item);
}

export async function removeGroupCurator(
    id: GroupCuratorId,
): Promise<GroupCuratorDetailServiceResult> {
    const item = await deactivateGroupCurator(id);

    return createGroupCuratorDetailServiceResult(item);
}

export async function restoreGroupCuratorById(
    id: GroupCuratorId,
): Promise<GroupCuratorDetailServiceResult> {
    const item = await restoreGroupCurator(id);

    return createGroupCuratorDetailServiceResult(item);
}

export async function makePrimaryGroupCurator(
    id: GroupCuratorId,
): Promise<GroupCuratorDetailServiceResult> {
    const item = await setPrimaryGroupCurator(id);

    return createGroupCuratorDetailServiceResult(item);
}

function createGroupCuratorDetailServiceResult(
    item: GroupCuratorDto,
): GroupCuratorDetailServiceResult {
    return {
        item,
        viewItem: mapGroupCuratorToListItem(item),
        details: mapGroupCuratorToDetails(item),
    };
}
