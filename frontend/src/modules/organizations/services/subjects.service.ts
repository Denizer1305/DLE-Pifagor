import {
    createSubject as createSubjectApi,
    deactivateSubject,
    getSubject,
    getSubjects,
    restoreSubject,
    updateSubject as updateSubjectApi,
} from "../api";
import {
    mapSubjectToDetails,
    mapSubjectToListItem,
    mapSubjectsToListItems,
} from "../mappers";
import { mapSubjectFormToPayload } from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    OrganizationDetailsView,
    SubjectDto,
    SubjectFormModel,
    SubjectId,
    SubjectListItemView,
    SubjectListQuery,
} from "../types";

export interface SubjectDetailServiceResult {
    item: SubjectDto;
    viewItem: SubjectListItemView;
    details: OrganizationDetailsView;
}

export async function loadSubjects(
    query?: SubjectListQuery,
) {
    const response = await getSubjects(query);

    return createListServiceResult(
        response,
        mapSubjectsToListItems,
    );
}

export async function loadSubjectDetails(
    id: SubjectId,
): Promise<SubjectDetailServiceResult> {
    const item = await getSubject(id);

    return createSubjectDetailServiceResult(item);
}

export async function createSubject(
    form: SubjectFormModel,
): Promise<SubjectDetailServiceResult> {
    const item = await createSubjectApi(
        mapSubjectFormToPayload(form),
    );

    return createSubjectDetailServiceResult(item);
}

export async function updateSubject(
    id: SubjectId,
    form: SubjectFormModel,
): Promise<SubjectDetailServiceResult> {
    const item = await updateSubjectApi(
        id,
        mapSubjectFormToPayload(form),
    );

    return createSubjectDetailServiceResult(item);
}

export async function removeSubject(
    id: SubjectId,
): Promise<SubjectDetailServiceResult> {
    const item = await deactivateSubject(id);

    return createSubjectDetailServiceResult(item);
}

export async function restoreSubjectById(
    id: SubjectId,
): Promise<SubjectDetailServiceResult> {
    const item = await restoreSubject(id);

    return createSubjectDetailServiceResult(item);
}

function createSubjectDetailServiceResult(
    item: SubjectDto,
): SubjectDetailServiceResult {
    return {
        item,
        viewItem: mapSubjectToListItem(item),
        details: mapSubjectToDetails(item),
    };
}
