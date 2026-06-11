import {
    deleteApi,
    getApiDetail,
    getApiList,
    patchApi,
    postApi,
} from "./organizations-http.api";
import type {
    DepartmentDto,
    DepartmentId,
    DepartmentListQuery,
    DepartmentWritePayload,
} from "../types";

const DEPARTMENTS_URL = "/organizations/admin/departments/";

function getDepartmentUrl(id: DepartmentId): string {
    return `${DEPARTMENTS_URL}${id}/`;
}

export function getDepartments(
    query?: DepartmentListQuery,
) {
    return getApiList<DepartmentDto>(DEPARTMENTS_URL, query);
}

export function getDepartment(
    id: DepartmentId,
) {
    return getApiDetail<DepartmentDto>(getDepartmentUrl(id));
}

export function createDepartment(
    payload: DepartmentWritePayload,
) {
    return postApi<DepartmentDto, DepartmentWritePayload>(
        DEPARTMENTS_URL,
        payload,
    );
}

export function updateDepartment(
    id: DepartmentId,
    payload: DepartmentWritePayload,
) {
    return patchApi<DepartmentDto, DepartmentWritePayload>(
        getDepartmentUrl(id),
        payload,
    );
}

export function deactivateDepartment(
    id: DepartmentId,
) {
    return deleteApi<DepartmentDto>(getDepartmentUrl(id));
}

export function restoreDepartment(
    id: DepartmentId,
) {
    return postApi<DepartmentDto>(
        `${getDepartmentUrl(id)}restore/`,
    );
}
