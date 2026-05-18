import {
    fetchPublicOrganizationTeachers,
    fetchPublicOrganizations,
} from "@/api/modules/organizations.api";

import {
    chooseDefaultOrganization,
    mapPublicOrganizationFromApi,
    mapPublicTeacherFromApi,
} from "../mappers/publicTeachers.mapper";
import type {
    PublicOrganization,
    PublicTeacher,
} from "../types/public-teachers.types";

export interface PublicTeachersInitialData {
    organizations: PublicOrganization[];
    defaultOrganizationSlug: string;
    teachers: PublicTeacher[];
}

export async function getPublicOrganizations(): Promise<PublicOrganization[]> {
    const organizations = await fetchPublicOrganizations();

    return organizations.map(mapPublicOrganizationFromApi);
}

export async function getPublicTeachersByOrganization(
    organizationSlug: string,
): Promise<PublicTeacher[]> {
    const teachers = await fetchPublicOrganizationTeachers(organizationSlug);

    return teachers.map(mapPublicTeacherFromApi);
}

export async function getPublicTeachersInitialData(): Promise<PublicTeachersInitialData> {
    const organizations = await getPublicOrganizations();
    const defaultOrganization = chooseDefaultOrganization(organizations);

    if (!defaultOrganization) {
        return {
            organizations: [],
            defaultOrganizationSlug: "",
            teachers: [],
        };
    }

    const teachers = await getPublicTeachersByOrganization(defaultOrganization.slug);

    return {
        organizations,
        defaultOrganizationSlug: defaultOrganization.slug,
        teachers,
    };
}
