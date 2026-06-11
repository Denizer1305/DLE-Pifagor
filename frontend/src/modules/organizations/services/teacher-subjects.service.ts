import {
    createTeacherSubject as createTeacherSubjectApi,
    deactivateTeacherSubject,
    getTeacherSubject,
    getTeacherSubjects,
    restoreTeacherSubject,
    setPrimaryTeacherSubject,
    updateTeacherSubject as updateTeacherSubjectApi,
} from "../api";
import {
    mapTeacherSubjectToDetails,
    mapTeacherSubjectToListItem,
    mapTeacherSubjectsToListItems,
} from "../mappers";
import { mapTeacherSubjectFormToPayload } from "../utils";
import { createListServiceResult } from "./organization-service.helpers";
import type {
    OrganizationDetailsView,
    TeacherSubjectDto,
    TeacherSubjectFormModel,
    TeacherSubjectId,
    TeacherSubjectListItemView,
    TeacherSubjectListQuery,
} from "../types";

export interface TeacherSubjectDetailServiceResult {
    item: TeacherSubjectDto;
    viewItem: TeacherSubjectListItemView;
    details: OrganizationDetailsView;
}

export async function loadTeacherSubjects(
    query?: TeacherSubjectListQuery,
) {
    const response = await getTeacherSubjects(query);

    return createListServiceResult(
        response,
        mapTeacherSubjectsToListItems,
    );
}

export async function loadTeacherSubjectDetails(
    id: TeacherSubjectId,
): Promise<TeacherSubjectDetailServiceResult> {
    const item = await getTeacherSubject(id);

    return createTeacherSubjectDetailServiceResult(item);
}

export async function createTeacherSubject(
    form: TeacherSubjectFormModel,
): Promise<TeacherSubjectDetailServiceResult> {
    const item = await createTeacherSubjectApi(
        mapTeacherSubjectFormToPayload(form),
    );

    return createTeacherSubjectDetailServiceResult(item);
}

export async function updateTeacherSubject(
    id: TeacherSubjectId,
    form: TeacherSubjectFormModel,
): Promise<TeacherSubjectDetailServiceResult> {
    const item = await updateTeacherSubjectApi(
        id,
        mapTeacherSubjectFormToPayload(form),
    );

    return createTeacherSubjectDetailServiceResult(item);
}

export async function removeTeacherSubject(
    id: TeacherSubjectId,
): Promise<TeacherSubjectDetailServiceResult> {
    const item = await deactivateTeacherSubject(id);

    return createTeacherSubjectDetailServiceResult(item);
}

export async function restoreTeacherSubjectById(
    id: TeacherSubjectId,
): Promise<TeacherSubjectDetailServiceResult> {
    const item = await restoreTeacherSubject(id);

    return createTeacherSubjectDetailServiceResult(item);
}

export async function makePrimaryTeacherSubject(
    id: TeacherSubjectId,
): Promise<TeacherSubjectDetailServiceResult> {
    const item = await setPrimaryTeacherSubject(id);

    return createTeacherSubjectDetailServiceResult(item);
}

function createTeacherSubjectDetailServiceResult(
    item: TeacherSubjectDto,
): TeacherSubjectDetailServiceResult {
    return {
        item,
        viewItem: mapTeacherSubjectToListItem(item),
        details: mapTeacherSubjectToDetails(item),
    };
}
