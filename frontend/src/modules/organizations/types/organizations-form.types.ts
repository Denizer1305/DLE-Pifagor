import type {
    DepartmentId,
    IsoDateString,
    IsoDateTimeString,
    OrganizationId,
    StudyFormApi,
    StudyGroupId,
    StudyGroupStatusApi,
    SubjectId,
    TeacherEmploymentTypeApi,
    UserId,
} from "./organizations-api.types";

export interface OrganizationFormModel {
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
    isPublic: boolean;
    isDefaultPublic: boolean;
}

export interface DepartmentFormModel {
    organizationId: OrganizationId | null;
    name: string;
    shortName: string;
    code: string;
    description: string;
}

export interface StudyGroupFormModel {
    organizationId: OrganizationId | null;
    departmentId: DepartmentId | null;
    name: string;
    code: string;
    description: string;
    admissionYear: number | null;
    graduationYear: number | null;
    courseNumber: number | null;
    studyForm: StudyFormApi;
    status: StudyGroupStatusApi;
}

export interface SubjectFormModel {
    name: string;
    shortName: string;
    code: string;
    description: string;
}

export interface TeacherOrganizationFormModel {
    teacherId: UserId | null;
    organizationId: OrganizationId | null;
    position: string;
    employmentType: TeacherEmploymentTypeApi;
    isPrimary: boolean;
    isActive: boolean;
    notes: string;
    startsAt: IsoDateString | null;
    endsAt: IsoDateString | null;
}

export interface TeacherSubjectFormModel {
    teacherId: UserId | null;
    subjectId: SubjectId | null;
    isPrimary: boolean;
    isActive: boolean;
    notes: string;
}

export interface GroupCuratorFormModel {
    groupId: StudyGroupId | null;
    teacherId: UserId | null;
    isPrimary: boolean;
    isActive: boolean;
    notes: string;
    startsAt: IsoDateString | null;
    endsAt: IsoDateString | null;
}

export interface CodeFormModel {
    rawCode: string;
    expiresAt: IsoDateTimeString | null;
}

export interface JoinRequestReviewFormModel {
    comment: string;
}

export type OrganizationFormMode = "create" | "edit";

export interface OrganizationFormState<TModel> {
    mode: OrganizationFormMode;
    model: TModel;
    isSubmitting: boolean;
    errors: Partial<Record<keyof TModel | "detail", string>>;
}
