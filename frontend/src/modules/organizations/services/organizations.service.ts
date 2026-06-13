import {
    clearTeacherRegistrationCode,
    createOrganization as createOrganizationApi,
    deactivateOrganization,
    disableTeacherRegistrationCode,
    getOrganization,
    getOrganizations,
    restoreOrganization,
    setTeacherRegistrationCode,
    updateOrganization as updateOrganizationApi,
} from "../api";
import {
    mapOrganizationToDetails,
    mapOrganizationToListItem,
    mapOrganizationsToListItems,
} from "../mappers";
import {
    mapCodeFormToPayload,
    mapOrganizationFormToPayload,
} from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    CodeFormModel,
    OrganizationDetailsView,
    OrganizationDto,
    OrganizationFormModel,
    OrganizationId,
    OrganizationListItemView,
    OrganizationListQuery,
    TeacherRegistrationCodeResponse,
} from "../types";

export interface OrganizationDetailServiceResult {
    item: OrganizationDto;
    viewItem: OrganizationListItemView;
    details: OrganizationDetailsView;
}

export async function loadOrganizations(
    query?: OrganizationListQuery,
) {
    const response = await getOrganizations(query);

    return createListServiceResult(
        response,
        mapOrganizationsToListItems,
    );
}

export async function loadOrganizationDetails(
    id: OrganizationId,
): Promise<OrganizationDetailServiceResult> {
    const item = await getOrganization(id);

    return createOrganizationDetailServiceResult(item);
}

export async function createOrganization(
    form: OrganizationFormModel,
): Promise<OrganizationDetailServiceResult> {
    const item = await createOrganizationApi(
        mapOrganizationFormToPayload(form),
    );

    return createOrganizationDetailServiceResult(item);
}

export async function updateOrganization(
    id: OrganizationId,
    form: OrganizationFormModel,
): Promise<OrganizationDetailServiceResult> {
    const item = await updateOrganizationApi(
        id,
        mapOrganizationFormToPayload(form),
    );

    return createOrganizationDetailServiceResult(item);
}

export async function removeOrganization(
    id: OrganizationId,
): Promise<OrganizationDetailServiceResult> {
    const item = await deactivateOrganization(id);

    return createOrganizationDetailServiceResult(item);
}

export async function restoreOrganizationById(
    id: OrganizationId,
): Promise<OrganizationDetailServiceResult> {
    const item = await restoreOrganization(id);

    return createOrganizationDetailServiceResult(item);
}

export async function saveTeacherRegistrationCode(
    id: OrganizationId,
    form: CodeFormModel,
): Promise<TeacherRegistrationCodeResponse> {
    return setTeacherRegistrationCode(
        id,
        mapCodeFormToPayload(form),
    );
}

export async function disableOrganizationTeacherRegistrationCode(
    id: OrganizationId,
): Promise<OrganizationDetailServiceResult> {
    const item = await disableTeacherRegistrationCode(id);

    return createOrganizationDetailServiceResult(item);
}

export async function clearOrganizationTeacherRegistrationCode(
    id: OrganizationId,
): Promise<OrganizationDetailServiceResult> {
    const item = await clearTeacherRegistrationCode(id);

    return createOrganizationDetailServiceResult(item);
}

function createOrganizationDetailServiceResult(
    item: OrganizationDto,
): OrganizationDetailServiceResult {
    return {
        item,
        viewItem: mapOrganizationToListItem(item),
        details: mapOrganizationToDetails(item),
    };
}
