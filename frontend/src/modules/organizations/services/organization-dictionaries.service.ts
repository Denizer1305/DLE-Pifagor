import {
    getDepartments,
    getOrganizations,
    getStudyGroups,
    getSubjects,
    getTeacherOrganizations,
} from "../api";
import { mapApiListResponse } from "../mappers";
import type {
    DepartmentDictionaryItem,
    OrganizationModuleDictionaries,
    StudyGroupDictionaryItem,
    TeacherDictionaryItem,
} from "../types";

export async function loadOrganizationDictionaries(): Promise<OrganizationModuleDictionaries> {
    const [
        organizationsResponse,
        departmentsResponse,
        studyGroupsResponse,
        subjectsResponse,
        teacherOrganizationsResponse,
    ] = await Promise.all([
        getOrganizations({
            is_active: true,
        }),
        getDepartments({
            is_active: true,
        }),
        getStudyGroups({
            is_active: true,
        }),
        getSubjects({
            is_active: true,
        }),
        getTeacherOrganizations({
            is_active: true,
        }),
    ]);

    const organizations = mapApiListResponse(organizationsResponse).items;
    const departments = mapApiListResponse(departmentsResponse).items;
    const studyGroups = mapApiListResponse(studyGroupsResponse).items;
    const subjects = mapApiListResponse(subjectsResponse).items;
    const teacherOrganizations = mapApiListResponse(
        teacherOrganizationsResponse,
    ).items;

    return {
        organizations,
        departments: departments.map((department): DepartmentDictionaryItem => {
            return {
                id: department.id,
                organizationId: department.organization.id,
                name: department.name,
                shortName: department.short_name,
                code: department.code,
            };
        }),
        studyGroups: studyGroups.map((group): StudyGroupDictionaryItem => {
            return {
                id: group.id,
                organizationId: group.organization.id,
                departmentId: group.department?.id ?? null,
                name: group.name,
                code: group.code,
            };
        }),
        subjects,
        teachers: createTeacherDictionary(teacherOrganizations),
    };
}

function createTeacherDictionary(
    teacherOrganizations: Array<{
        teacher: number;
        teacher_full_name?: string;
        teacher_email?: string;
        teacher_phone?: string;
    }>,
): TeacherDictionaryItem[] {
    const teachersMap = new Map<number, TeacherDictionaryItem>();

    teacherOrganizations.forEach((teacherOrganization) => {
        if (teachersMap.has(teacherOrganization.teacher)) {
            return;
        }

        teachersMap.set(teacherOrganization.teacher, {
            id: teacherOrganization.teacher,
            fullName:
                teacherOrganization.teacher_full_name
                || `Преподаватель #${teacherOrganization.teacher}`,
            email: teacherOrganization.teacher_email || "",
            phone: teacherOrganization.teacher_phone || "",
        });
    });

    return Array.from(teachersMap.values());
}
