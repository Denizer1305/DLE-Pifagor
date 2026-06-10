import { fetchPublicTeachersPage } from "@/modules/public/api/public-teachers.api";

import { mapPublicTeachersPage } from "../mappers/publicTeachers.mapper";
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
    const response = await fetchPublicTeachersPage();
    const pageData = mapPublicTeachersPage(response);

    return pageData.organization ? [pageData.organization] : [];
}

export async function getPublicTeachersByOrganization(
    _organizationSlug: string,
): Promise<PublicTeacher[]> {
    const response = await fetchPublicTeachersPage();
    const pageData = mapPublicTeachersPage(response);

    return pageData.teachers;
}

export async function getPublicTeachersInitialData(): Promise<PublicTeachersInitialData> {
    const response = await fetchPublicTeachersPage();
    const pageData = mapPublicTeachersPage(response);
    const organizations = pageData.organization ? [pageData.organization] : [];

    if (!pageData.organization) {
        return {
            organizations: [],
            defaultOrganizationSlug: "",
            teachers: [],
        };
    }

    return {
        organizations,
        defaultOrganizationSlug: pageData.organization.slug,
        teachers: pageData.teachers,
    };
}
