import fallbackTeacherImage from "@/assets/image/avatars/foto_teachers.webp";
import type {
    PublicTeacher,
    PublicTeacherApi,
    PublicTeachersMeta,
    PublicOrganizationApi,
    PublicTeachersOrganization,
    PublicTeachersPageData,
    PublicTeachersSubject,
} from "@/modules/public/types/public-teachers.types";
import type {
    PublicTeacherDto,
    PublicTeachersMetaDto,
    PublicTeachersOrganizationDto,
    PublicTeachersPageDto,
    PublicTeachersSubjectDto,
} from "@/modules/public/api/public-teachers.api";

function mapOrganization(
    dto: PublicTeachersOrganizationDto | null,
): PublicTeachersOrganization | null {
    if (!dto) {
        return null;
    }

    return {
        id: dto.id,
        name: dto.name,
        shortName: dto.short_name,
        slug: dto.slug,
        code: dto.code,
        description: dto.description,
        city: dto.city,
        address: dto.address,
        phone: dto.phone,
        email: dto.email,
        website: dto.website,
        logoUrl: dto.logo_url,
        isDefaultPublic: dto.is_default_public,
    };
}

function mapSubject(dto: PublicTeachersSubjectDto): PublicTeachersSubject {
    return {
        id: dto.id,
        name: dto.name,
        shortName: dto.short_name,
        code: dto.code,
    };
}

function getPrimarySubject(dto: PublicTeacherDto): string {
    const primarySubject = dto.subjects.find((subject) => subject.is_primary);
    const subject = primarySubject || dto.subjects[0];

    if (!subject) {
        return "Предметы не указаны";
    }

    return subject.short_name || subject.name;
}

function mapTeacher(dto: PublicTeacherDto): PublicTeacher {
    const tags = dto.subjects.map((subject) => {
        return subject.short_name || subject.name;
    });

    if (dto.experience_years) {
        tags.push(`${dto.experience_years} лет опыта`);
    }

    return {
        id: dto.id,
        name: dto.full_name,
        role: dto.position || "Преподаватель",
        subject: getPrimarySubject(dto),
        direction: dto.subjects.length
            ? dto.subjects.map((subject) => subject.name).join(", ")
            : "Учебное направление не указано",
        description: dto.description || "Преподаватель ЦОС «Пифагор».",
        image: {
            src: dto.photo_url || fallbackTeacherImage,
            alt: dto.full_name,
        },
        tags,
        awards: dto.achievements.slice(0, 5),
        experienceYears: dto.experience_years,
        department: dto.department
            ? {
                id: dto.department.id,
                name: dto.department.name,
                shortName: dto.department.short_name,
                code: dto.department.code,
            }
            : null,
    };
}

function mapMeta(dto: PublicTeachersMetaDto): PublicTeachersMeta {
    return {
        teachersCount: dto.teachers_count,
        subjectsCount: dto.subjects_count,
        isFallback: dto.is_fallback,
        search: dto.search,
        subject: dto.subject,
        position: dto.position,
        message: dto.message,
    };
}

export function mapPublicTeachersPage(
    dto: PublicTeachersPageDto,
): PublicTeachersPageData {
    return {
        organization: mapOrganization(dto.organization),
        subjects: dto.subjects.map(mapSubject),
        teachers: dto.teachers.map(mapTeacher),
        meta: mapMeta(dto.meta),
    };
}

export function mapPublicOrganizationFromApi(
    apiOrganization: PublicOrganizationApi,
): PublicTeachersOrganization {
    return {
        id: apiOrganization.id,
        name: apiOrganization.name,
        shortName: apiOrganization.short_name || apiOrganization.name,
        slug: apiOrganization.slug || String(apiOrganization.id),
        code: apiOrganization.code || String(apiOrganization.id),
        description: apiOrganization.description || "",
        city: apiOrganization.city || "",
        address: apiOrganization.address || "",
        phone: apiOrganization.phone || "",
        email: apiOrganization.email || "",
        website: apiOrganization.website || "",
        logoUrl: apiOrganization.logo_url || "",
        isDefaultPublic: Boolean(apiOrganization.is_default_public),
    };
}

export function mapPublicTeacherFromApi(apiTeacher: PublicTeacherApi): PublicTeacher {
    const subjects = apiTeacher.subjects || [];
    const primarySubject = subjects.find((subject) => subject.is_primary) || subjects[0];
    const teacherName = apiTeacher.full_name || apiTeacher.name || "Преподаватель";
    const achievements = apiTeacher.achievements || apiTeacher.awards || [];

    return {
        id: apiTeacher.id,
        name: teacherName,
        role: apiTeacher.position || apiTeacher.role || "Преподаватель",
        subject:
            apiTeacher.subject ||
            primarySubject?.short_name ||
            primarySubject?.name ||
            "Предмет не указан",
        direction:
            apiTeacher.direction ||
            (subjects.length
                ? subjects.map((subject) => subject.name).join(", ")
                : "Учебное направление не указано"),
        description: apiTeacher.description || "Преподаватель ЦОС «Пифагор».",
        image: {
            src: apiTeacher.photo_url || apiTeacher.image || fallbackTeacherImage,
            alt: teacherName,
        },
        tags: subjects.map((subject) => subject.short_name || subject.name),
        awards: achievements.slice(0, 5),
        experienceYears: apiTeacher.experience_years || null,
        department: apiTeacher.department
            ? {
                id: apiTeacher.department.id,
                name: apiTeacher.department.name,
                shortName: apiTeacher.department.short_name,
                code: apiTeacher.department.code,
            }
            : null,
    };
}

export function chooseDefaultOrganization(
    organizations: PublicTeachersOrganization[],
): PublicTeachersOrganization | null {
    return (
        organizations.find((organization) => organization.isDefaultPublic) ||
        organizations[0] ||
        null
    );
}
