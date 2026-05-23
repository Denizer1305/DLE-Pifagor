import { httpClient } from "@/services/api/http.client";
import type {
    PublicOrganizationApi,
    PublicTeacherApi,
} from "@/modules/public/types/public-teachers.types";

const ORGANIZATIONS_BASE_URL = "/organizations";

export async function fetchPublicOrganizations(): Promise<PublicOrganizationApi[]> {
    const response = await httpClient.get<PublicOrganizationApi[]>(
        `${ORGANIZATIONS_BASE_URL}/public/`,
    );

    return response.data;
}

export async function fetchPublicOrganizationTeachers(
    organizationSlug: string,
): Promise<PublicTeacherApi[]> {
    const response = await httpClient.get<PublicTeacherApi[]>(
        `${ORGANIZATIONS_BASE_URL}/public/${organizationSlug}/teachers/`,
    );

    return response.data;
}
