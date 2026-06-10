import {
    createDepartment as createDepartmentApi,
    deactivateDepartment,
    getDepartment,
    getDepartments,
    restoreDepartment,
    updateDepartment as updateDepartmentApi,
} from "../api";
import {
    mapDepartmentToDetails,
    mapDepartmentToListItem,
    mapDepartmentsToListItems,
} from "../mappers";
import { mapDepartmentFormToPayload } from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    DepartmentDto,
    DepartmentFormModel,
    DepartmentId,
    DepartmentListItemView,
    DepartmentListQuery,
    OrganizationDetailsView,
} from "../types";

export interface DepartmentDetailServiceResult {
    item: DepartmentDto;
    viewItem: DepartmentListItemView;
    details: OrganizationDetailsView;
}

export async function loadDepartments(
    query?: DepartmentListQuery,
) {
    const response = await getDepartments(query);

    return createListServiceResult(
        response,
        mapDepartmentsToListItems,
    );
}

export async function loadDepartmentDetails(
    id: DepartmentId,
): Promise<DepartmentDetailServiceResult> {
    const item = await getDepartment(id);

    return createDepartmentDetailServiceResult(item);
}

export async function createDepartment(
    form: DepartmentFormModel,
): Promise<DepartmentDetailServiceResult> {
    const item = await createDepartmentApi(
        mapDepartmentFormToPayload(form),
    );

    return createDepartmentDetailServiceResult(item);
}

export async function updateDepartment(
    id: DepartmentId,
    form: DepartmentFormModel,
): Promise<DepartmentDetailServiceResult> {
    const item = await updateDepartmentApi(
        id,
        mapDepartmentFormToPayload(form),
    );

    return createDepartmentDetailServiceResult(item);
}

export async function removeDepartment(
    id: DepartmentId,
): Promise<DepartmentDetailServiceResult> {
    const item = await deactivateDepartment(id);

    return createDepartmentDetailServiceResult(item);
}

export async function restoreDepartmentById(
    id: DepartmentId,
): Promise<DepartmentDetailServiceResult> {
    const item = await restoreDepartment(id);

    return createDepartmentDetailServiceResult(item);
}

function createDepartmentDetailServiceResult(
    item: DepartmentDto,
): DepartmentDetailServiceResult {
    return {
        item,
        viewItem: mapDepartmentToListItem(item),
        details: mapDepartmentToDetails(item),
    };
}