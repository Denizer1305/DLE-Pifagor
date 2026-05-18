import type { RouteLocationRaw } from "vue-router";

export type PublicButtonVariant = "primary" | "secondary" | "light";

export interface PublicTeachersAction {
    label: string;
    to?: RouteLocationRaw;
    href?: string;
    variant?: PublicButtonVariant;
    icon?: string;
}

export interface TeachersHeroContent {
    badges: {
        icon: string;
        text: string;
    }[];
    title: string;
    subtitle: string;
    description: string;
    highlights: string[];
    actions: PublicTeachersAction[];
    logo: {
        src: string;
        alt: string;
    };
}

export interface TeachersCatalogContent {
    label: string;
    title: string;
    description: string;
    emptyTitle: string;
    emptyText: string;
    emptyOrganizationsTitle: string;
    emptyOrganizationsText: string;
    searchPlaceholder: string;
    subjectPlaceholder: string;
}

export interface TeachersCtaContent {
    title: string;
    text: string;
    note: string;
    actions: PublicTeachersAction[];
}

export interface TeachersPageContent {
    hero: TeachersHeroContent;
    catalog: TeachersCatalogContent;
    cta: TeachersCtaContent;
}

export interface PublicTeachersOrganization {
    id: number;
    name: string;
    shortName: string;
    slug: string;
    code: string;
    description: string;
    city: string;
    address: string;
    phone: string;
    email: string;
    website: string;
    logoUrl: string;
    isDefaultPublic: boolean;
}

export type PublicOrganization = PublicTeachersOrganization;

export interface PublicOrganizationApi {
    id: number;
    name: string;
    short_name?: string;
    slug?: string;
    code?: string;
    description?: string;
    city?: string;
    address?: string;
    phone?: string;
    email?: string;
    website?: string;
    logo_url?: string;
    is_default_public?: boolean;
}

export interface PublicTeachersSubject {
    id: number;
    name: string;
    shortName: string;
    code: string;
}

export interface PublicTeacher {
    id: number;
    name: string;
    role: string;
    subject: string;
    direction: string;
    description: string;
    image: {
        src: string;
        alt: string;
    };
    tags: string[];
    awards: string[];
    experienceYears: number | null;
    department: {
        id: number;
        name: string;
        shortName: string;
        code: string;
    } | null;
}

export interface PublicTeacherApi {
    id: number;
    full_name?: string;
    name?: string;
    position?: string;
    role?: string;
    description?: string;
    photo_url?: string;
    image?: string;
    subject?: string;
    direction?: string;
    subjects?: {
        id?: number;
        name: string;
        short_name?: string;
        code?: string;
        is_primary?: boolean;
    }[];
    achievements?: string[];
    awards?: string[];
    experience_years?: number | null;
    department?: {
        id: number;
        name: string;
        short_name: string;
        code: string;
    } | null;
}

export interface PublicTeachersMeta {
    teachersCount: number;
    subjectsCount: number;
    isFallback: boolean;
    search: string;
    subject: string;
    position: string;
    message?: string;
}

export interface PublicTeachersPageData {
    organization: PublicTeachersOrganization | null;
    subjects: PublicTeachersSubject[];
    teachers: PublicTeacher[];
    meta: PublicTeachersMeta;
}

export interface PublicTeachersQuery {
    search?: string;
    subject?: string;
    position?: string;
}
