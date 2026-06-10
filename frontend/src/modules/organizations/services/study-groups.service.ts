import {
    archiveStudyGroup,
    clearGroupJoinCode,
    createStudyGroup as createStudyGroupApi,
    disableGroupJoinCode,
    getStudyGroup,
    getStudyGroups,
    restoreStudyGroup,
    setGroupJoinCode,
    updateStudyGroup as updateStudyGroupApi,
} from "../api";
import {
    mapStudyGroupToDetails,
    mapStudyGroupToListItem,
    mapStudyGroupsToListItems,
} from "../mappers";
import {
    mapCodeFormToPayload,
    mapStudyGroupFormToPayload,
} from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    CodeFormModel,
    GroupJoinCodeResponse,
    OrganizationDetailsView,
    StudyGroupDto,
    StudyGroupFormModel,
    StudyGroupId,
    StudyGroupListItemView,
    StudyGroupListQuery,
} from "../types";

export interface StudyGroupDetailServiceResult {
    item: StudyGroupDto;
    viewItem: StudyGroupListItemView;
    details: OrganizationDetailsView;
}

export async function loadStudyGroups(
    query?: StudyGroupListQuery,
) {
    const response = await getStudyGroups(query);

    return createListServiceResult(
        response,
        mapStudyGroupsToListItems,
    );
}

export async function loadStudyGroupDetails(
    id: StudyGroupId,
): Promise<StudyGroupDetailServiceResult> {
    const item = await getStudyGroup(id);

    return createStudyGroupDetailServiceResult(item);
}

export async function createStudyGroup(
    form: StudyGroupFormModel,
): Promise<StudyGroupDetailServiceResult> {
    const item = await createStudyGroupApi(
        mapStudyGroupFormToPayload(form),
    );

    return createStudyGroupDetailServiceResult(item);
}

export async function updateStudyGroup(
    id: StudyGroupId,
    form: StudyGroupFormModel,
): Promise<StudyGroupDetailServiceResult> {
    const item = await updateStudyGroupApi(
        id,
        mapStudyGroupFormToPayload(form),
    );

    return createStudyGroupDetailServiceResult(item);
}

export async function removeStudyGroup(
    id: StudyGroupId,
): Promise<StudyGroupDetailServiceResult> {
    const item = await archiveStudyGroup(id);

    return createStudyGroupDetailServiceResult(item);
}

export async function restoreStudyGroupById(
    id: StudyGroupId,
): Promise<StudyGroupDetailServiceResult> {
    const item = await restoreStudyGroup(id);

    return createStudyGroupDetailServiceResult(item);
}

export async function saveGroupJoinCode(
    id: StudyGroupId,
    form: CodeFormModel,
): Promise<GroupJoinCodeResponse> {
    return setGroupJoinCode(
        id,
        mapCodeFormToPayload(form),
    );
}

export async function disableStudyGroupJoinCode(
    id: StudyGroupId,
): Promise<StudyGroupDetailServiceResult> {
    const item = await disableGroupJoinCode(id);

    return createStudyGroupDetailServiceResult(item);
}

export async function clearStudyGroupJoinCode(
    id: StudyGroupId,
): Promise<StudyGroupDetailServiceResult> {
    const item = await clearGroupJoinCode(id);

    return createStudyGroupDetailServiceResult(item);
}

function createStudyGroupDetailServiceResult(
    item: StudyGroupDto,
): StudyGroupDetailServiceResult {
    return {
        item,
        viewItem: mapStudyGroupToListItem(item),
        details: mapStudyGroupToDetails(item),
    };
}