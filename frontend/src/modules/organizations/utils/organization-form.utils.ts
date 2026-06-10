import { normalizeRussianPhone } from "@/modules/auth/composables/usePhoneMask";

import type {
    CodeSetPayload,
    DepartmentWritePayload,
    GroupCuratorWritePayload,
    JoinRequestReviewPayload,
    OrganizationWritePayload,
    StudyGroupWritePayload,
    SubjectWritePayload,
    TeacherOrganizationWritePayload,
    TeacherSubjectWritePayload,
} from "../types/organizations-api.types";
import type {
    CodeFormModel,
    DepartmentFormModel,
    GroupCuratorFormModel,
    JoinRequestReviewFormModel,
    OrganizationFormModel,
    StudyGroupFormModel,
    SubjectFormModel,
    TeacherOrganizationFormModel,
    TeacherSubjectFormModel,
} from "../types/organizations-form.types";

function trimValue(value: string): string {
    return value.trim();
}

function nullableNumber(value: number | null): number | null {
    return typeof value === "number" ? value : null;
}

function nullableString(value: string | null): string | null {
    if (value === null) {
        return null;
    }

    const trimmedValue = value.trim();

    return trimmedValue || null;
}

export function createEmptyOrganizationForm(): OrganizationFormModel {
    return {
        name: "",
        shortName: "",
        slug: "",
        code: "",
        description: "",
        city: "",
        address: "",
        phone: "",
        email: "",
        website: "",
        isPublic: true,
        isDefaultPublic: false,
    };
}

export function createEmptyDepartmentForm(): DepartmentFormModel {
    return {
        organizationId: null,
        name: "",
        shortName: "",
        code: "",
        description: "",
    };
}

export function createEmptyStudyGroupForm(): StudyGroupFormModel {
    return {
        organizationId: null,
        departmentId: null,
        name: "",
        code: "",
        description: "",
        admissionYear: null,
        graduationYear: null,
        courseNumber: null,
        studyForm: "full_time",
        status: "active",
    };
}

export function createEmptySubjectForm(): SubjectFormModel {
    return {
        name: "",
        shortName: "",
        code: "",
        description: "",
    };
}

export function createEmptyTeacherOrganizationForm(): TeacherOrganizationFormModel {
    return {
        teacherId: null,
        organizationId: null,
        position: "",
        employmentType: "full_time",
        isPrimary: false,
        isActive: true,
        notes: "",
        startsAt: null,
        endsAt: null,
    };
}

export function createEmptyTeacherSubjectForm(): TeacherSubjectFormModel {
    return {
        teacherId: null,
        subjectId: null,
        isPrimary: false,
        isActive: true,
        notes: "",
    };
}

export function createEmptyGroupCuratorForm(): GroupCuratorFormModel {
    return {
        groupId: null,
        teacherId: null,
        isPrimary: false,
        isActive: true,
        notes: "",
        startsAt: null,
        endsAt: null,
    };
}

export function createEmptyCodeForm(): CodeFormModel {
    return {
        rawCode: "",
        expiresAt: null,
    };
}

export function createEmptyJoinRequestReviewForm(): JoinRequestReviewFormModel {
    return {
        comment: "",
    };
}

export function mapOrganizationFormToPayload(
    form: OrganizationFormModel,
): OrganizationWritePayload {
    return {
        name: trimValue(form.name),
        short_name: trimValue(form.shortName),
        slug: trimValue(form.slug),
        code: trimValue(form.code),
        description: trimValue(form.description),
        city: trimValue(form.city),
        address: trimValue(form.address),
        phone: normalizeRussianPhone(form.phone),
        email: trimValue(form.email),
        website: trimValue(form.website),
        is_public: form.isPublic,
        is_default_public: form.isDefaultPublic,
    };
}

export function mapDepartmentFormToPayload(
    form: DepartmentFormModel,
): DepartmentWritePayload {
    return {
        organization_id: form.organizationId ?? undefined,
        name: trimValue(form.name),
        short_name: trimValue(form.shortName),
        code: trimValue(form.code),
        description: trimValue(form.description),
    };
}

export function mapStudyGroupFormToPayload(
    form: StudyGroupFormModel,
): StudyGroupWritePayload {
    return {
        organization_id: form.organizationId ?? undefined,
        department_id: form.departmentId,
        name: trimValue(form.name),
        code: trimValue(form.code),
        description: trimValue(form.description),
        admission_year: nullableNumber(form.admissionYear),
        graduation_year: nullableNumber(form.graduationYear),
        course_number: nullableNumber(form.courseNumber),
        study_form: form.studyForm,
        status: form.status,
    };
}

export function mapSubjectFormToPayload(
    form: SubjectFormModel,
): SubjectWritePayload {
    return {
        name: trimValue(form.name),
        short_name: trimValue(form.shortName),
        code: trimValue(form.code),
        description: trimValue(form.description),
    };
}

export function mapTeacherOrganizationFormToPayload(
    form: TeacherOrganizationFormModel,
): TeacherOrganizationWritePayload {
    return {
        teacher_id: form.teacherId ?? undefined,
        organization_id: form.organizationId ?? undefined,
        position: trimValue(form.position),
        employment_type: form.employmentType,
        is_primary: form.isPrimary,
        is_active: form.isActive,
        notes: trimValue(form.notes),
        starts_at: nullableString(form.startsAt),
        ends_at: nullableString(form.endsAt),
    };
}

export function mapTeacherSubjectFormToPayload(
    form: TeacherSubjectFormModel,
): TeacherSubjectWritePayload {
    return {
        teacher_id: form.teacherId ?? undefined,
        subject_id: form.subjectId ?? undefined,
        is_primary: form.isPrimary,
        is_active: form.isActive,
        notes: trimValue(form.notes),
    };
}

export function mapGroupCuratorFormToPayload(
    form: GroupCuratorFormModel,
): GroupCuratorWritePayload {
    return {
        group_id: form.groupId ?? undefined,
        teacher_id: form.teacherId ?? undefined,
        is_primary: form.isPrimary,
        is_active: form.isActive,
        notes: trimValue(form.notes),
        starts_at: nullableString(form.startsAt),
        ends_at: nullableString(form.endsAt),
    };
}

export function mapCodeFormToPayload(form: CodeFormModel): CodeSetPayload {
    return {
        raw_code: trimValue(form.rawCode),
        expires_at: form.expiresAt,
    };
}

export function mapJoinRequestReviewFormToPayload(
    form: JoinRequestReviewFormModel,
): JoinRequestReviewPayload {
    return {
        comment: trimValue(form.comment),
    };
}
