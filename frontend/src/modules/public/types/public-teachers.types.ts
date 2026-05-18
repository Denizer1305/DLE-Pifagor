export interface PublicOrganizationApi {
    id: number | string;
    name?: string | null;
    short_name?: string | null;
    description?: string | null;
    city?: string | null;
    logo_url?: string | null;
}

export interface PublicTeacherApi {
    id: number | string;
    organization_id?: number | string | null;
    name?: string | null;
    role?: string | null;
    subject?: string | null;
    direction?: string | null;
    image?: string | null;
    cover_image?: string | null;
    avatar?: string | null;
    description?: string | null;
    education?: string | null;
    experience?: string | number | null;
    awards?: string[] | string | null;
    tags?: string[] | string | null;
}

export interface PublicOrganization {
    slug: string;
    id: number | string;
    name: string;
    shortName: string;
    description: string;
    logoUrl: string;
    isDefault: boolean;
}

export interface PublicTeacher {
    id: string;
    sourceId: number | string;
    organizationSlug: string;
    name: string;
    role: string;
    subject: string;
    direction: string;
    image: {
        src: string;
        alt: string;
    };
    description: string;
    education: string;
    experience: string | number | null;
    awards: string[];
    tags: string[];
}
