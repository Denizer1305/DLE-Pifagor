import {
    createTeacherOrganization as createTeacherOrganizationApi,
    deactivateTeacherOrganization,
    getTeacherOrganization,
    getTeacherOrganizations,
    restoreTeacherOrganization,
    setPrimaryTeacherOrganization,
    updateTeacherOrganization as updateTeacherOrganizationApi,
} from "../api";
import {
    mapTeacherOrganizationToDetails,
    mapTeacherOrganizationToListItem,
    mapTeacherOrganizationsToListItems,
} from "../mappers";
import { mapTeacherOrganizationFormToPayload } from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    OrganizationDetailsView,
    TeacherOrganizationDto,
    TeacherOrganizationFormModel,
    TeacherOrganizationId,
    TeacherOrganizationListItemView,
    TeacherOrganizationListQuery,
} from "../types";

export interface TeacherOrganizationDetailServiceResult {
    item: TeacherOrganizationDto;
    viewItem: TeacherOrganizationListItemView;
    details: OrganizationDetailsView;
}

export async function loadTeacherOrganizations(
    query?: TeacherOrganizationListQuery,
) {
    const response = await getTeacherOrganizations(query);

    return createListServiceResult(
        response,
        mapTeacherOrganizationsToListItems,
    );
}

export async function loadTeacherOrganizationDetails(
    id: TeacherOrganizationId,
): Promise<TeacherOrganizationDetailServiceResult> {
    const item = await getTeacherOrganization(id);

    return createTeacherOrganizationDetailServiceResult(item);
}

export async function createTeacherOrganization(
    form: TeacherOrganizationFormModel,
): Promise<TeacherOrganizationDetailServiceResult> {
    const item = await createTeacherOrganizationApi(
        mapTeacherOrganizationFormToPayload(form),
    );

    return createTeacherOrganizationDetailServiceResult(item);
}

export async function updateTeacherOrganization(
    id: TeacherOrganizationId,
    form: TeacherOrganizationFormModel,
): Promise<TeacherOrganizationDetailServiceResult> {
    const item = await updateTeacherOrganizationApi(
        id,
        mapTeacherOrganizationFormToPayload(form),
    );

    return createTeacherOrganizationDetailServiceResult(item);
}

export async function removeTeacherOrganization(
    id: TeacherOrganizationId,
): Promise<TeacherOrganizationDetailServiceResult> {
    const item = await deactivateTeacherOrganization(id);

    return createTeacherOrganizationDetailServiceResult(item);
}

export async function restoreTeacherOrganizationById(
    id: TeacherOrganizationId,
): Promise<TeacherOrganizationDetailServiceResult> {
    const item = await restoreTeacherOrganization(id);

    return createTeacherOrganizationDetailServiceResult(item);
}

export async function makePrimaryTeacherOrganization(
    id: TeacherOrganizationId,
): Promise<TeacherOrganizationDetailServiceResult> {
    const item = await setPrimaryTeacherOrganization(id);

    return createTeacherOrganizationDetailServiceResult(item);
}

function createTeacherOrganizationDetailServiceResult(
    item: TeacherOrganizationDto,
): TeacherOrganizationDetailServiceResult {
    return {
        item,
        viewItem: mapTeacherOrganizationToListItem(item),
        details: mapTeacherOrganizationToDetails(item),
    };
}
