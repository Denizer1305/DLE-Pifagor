import { httpClient } from "@/services/api/http.client";
import type { PublicTeachersQuery } from "@/modules/public/types/public-teachers.types";

export interface PublicTeachersOrganizationDto {
    id: number;
    name: string;
    short_name: string;
    slug: string;
    code: string;
    description: string;
    city: string;
    address: string;
    phone: string;
    email: string;
    website: string;
    logo_url: string;
    is_default_public: boolean;
}

export interface PublicTeachersSubjectDto {
    id: number;
    name: string;
    short_name: string;
    code: string;
}

export interface PublicTeacherDto {
    id: number;
    full_name: string;
    position: string;
    description: string;
    photo_url: string;
    department: {
        id: number;
        name: string;
        short_name: string;
        code: string;
    } | null;
    subjects: {
        id: number;
        name: string;
        short_name: string;
        code: string;
        is_primary: boolean;
    }[];
    achievements: string[];
    experience_years: number | null;
}

export interface PublicTeachersMetaDto {
    teachers_count: number;
    subjects_count: number;
    is_fallback: boolean;
    search: string;
    subject: string;
    position: string;
    message?: string;
}

export interface PublicTeachersPageDto {
    organization: PublicTeachersOrganizationDto | null;
    subjects: PublicTeachersSubjectDto[];
    teachers: PublicTeacherDto[];
    meta: PublicTeachersMetaDto;
}

const PUBLIC_TEACHERS_URL = "/organizations/public/teachers/";

export async function fetchPublicTeachersPage(
    query: PublicTeachersQuery = {},
): Promise<PublicTeachersPageDto> {
    const response = await httpClient.get<PublicTeachersPageDto>(
        PUBLIC_TEACHERS_URL,
        {
            params: {
                search: query.search || undefined,
                subject: query.subject || undefined,
                position: query.position || undefined,
            },
        },
    );

    return response.data;
}