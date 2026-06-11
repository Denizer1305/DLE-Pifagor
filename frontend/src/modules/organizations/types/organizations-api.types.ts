export type OrganizationId = number;
export type DepartmentId = number;
export type StudyGroupId = number;
export type SubjectId = number;
export type UserId = number;
export type TeacherOrganizationId = number;
export type TeacherSubjectId = number;
export type GroupCuratorId = number;
export type JoinRequestId = number;

export type IsoDateString = string;
export type IsoDateTimeString = string;

export interface PaginatedApiResponse<TItem> {
    count: number;
    next: string | null;
    previous: string | null;
    results: TItem[];
}

export type ApiListResponse<TItem> = TItem[] | PaginatedApiResponse<TItem>;

export interface ApiListQuery {
    search?: string;
    ordering?: string;
    page?: number;
    page_size?: number;
}

export interface OrganizationListQuery extends ApiListQuery {
    is_active?: boolean;
    is_public?: boolean;
    city?: string;
}

export interface DepartmentListQuery extends ApiListQuery {
    organization_id?: OrganizationId;
    is_active?: boolean;
}

export interface StudyGroupListQuery extends ApiListQuery {
    organization_id?: OrganizationId;
    department_id?: DepartmentId;
    is_active?: boolean;
    is_archived?: boolean;
    status?: StudyGroupStatusApi;
}

export interface SubjectListQuery extends ApiListQuery {
    is_active?: boolean;
}

export interface TeacherOrganizationListQuery extends ApiListQuery {
    teacher_id?: UserId;
    organization_id?: OrganizationId;
    is_active?: boolean;
    is_primary?: boolean;
}

export interface TeacherSubjectListQuery extends ApiListQuery {
    teacher_id?: UserId;
    subject_id?: SubjectId;
    organization_id?: OrganizationId;
    is_active?: boolean;
    is_primary?: boolean;
}

export interface GroupCuratorListQuery extends ApiListQuery {
    group_id?: StudyGroupId;
    teacher_id?: UserId;
    organization_id?: OrganizationId;
    is_active?: boolean;
    is_primary?: boolean;
}

export interface JoinRequestListQuery extends ApiListQuery {
    request_type?: JoinRequestTypeApi;
    status?: JoinRequestStatusApi;
    organization_id?: OrganizationId;
    department_id?: DepartmentId;
    group_id?: StudyGroupId;
}

export type StudyGroupStatusApi =
    | "active"
    | "archived"
    | "graduated"
    | "draft";

export type StudyFormApi =
    | "full_time"
    | "part_time"
    | "distance"
    | "mixed";

export type TeacherEmploymentTypeApi =
    | "full_time"
    | "part_time"
    | "contract"
    | "external";

export type JoinRequestTypeApi =
    | "teacher_to_organization"
    | "learner_to_group"
    | "guardian_to_learner";

export type JoinRequestStatusApi =
    | "pending"
    | "approved"
    | "rejected"
    | "cancelled"
    | "expired";

export interface UserShortDto {
    id: UserId;
    email: string;
    phone: string;
    first_name: string;
    last_name: string;
    middle_name: string;
    full_name?: string;
}

export interface OrganizationShortDto {
    id: OrganizationId;
    name: string;
    short_name: string;
    code: string;
    slug: string;
}

export interface DepartmentShortDto {
    id: DepartmentId;
    name: string;
    short_name: string;
    code: string;
}

export interface StudyGroupShortDto {
    id: StudyGroupId;
    name: string;
    code: string;
}

export interface SubjectShortDto {
    id: SubjectId;
    name: string;
    short_name: string;
    code: string;
}

export interface OrganizationDto {
    id: OrganizationId;
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
    logo: string | null;
    is_active: boolean;
    is_public: boolean;
    is_default_public: boolean;
    has_active_teacher_registration_code?: boolean;
    teacher_registration_code_is_active?: boolean;
    teacher_registration_code_expires_at?: IsoDateTimeString | null;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface DepartmentDto {
    id: DepartmentId;
    organization: OrganizationShortDto;
    name: string;
    short_name: string;
    code: string;
    description?: string;
    is_active: boolean;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface StudyGroupDto {
    id: StudyGroupId;
    organization: OrganizationShortDto;
    department: DepartmentShortDto | null;
    name: string;
    code: string;
    description?: string;
    admission_year: number | null;
    graduation_year: number | null;
    course_number?: number | null;
    study_form?: StudyFormApi;
    status: StudyGroupStatusApi;
    is_active: boolean;
    is_archived: boolean;
    has_active_join_code?: boolean;
    join_code_is_active?: boolean;
    join_code_expires_at?: IsoDateTimeString | null;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface SubjectDto {
    id: SubjectId;
    name: string;
    short_name: string;
    code: string;
    description: string;
    is_active: boolean;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface TeacherOrganizationDto {
    id: TeacherOrganizationId;
    teacher: UserId;
    teacher_full_name?: string;
    teacher_email?: string;
    teacher_phone?: string;
    organization: OrganizationShortDto;
    position: string;
    employment_type: TeacherEmploymentTypeApi;
    is_primary: boolean;
    is_active: boolean;
    notes?: string;
    starts_at?: IsoDateString | null;
    ends_at?: IsoDateString | null;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface TeacherSubjectDto {
    id: TeacherSubjectId;
    teacher: UserId;
    teacher_full_name?: string;
    teacher_email?: string;
    teacher_phone?: string;
    subject: SubjectShortDto;
    is_primary: boolean;
    is_active: boolean;
    notes: string;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface GroupCuratorDto {
    id: GroupCuratorId;
    group: StudyGroupShortDto;
    teacher: UserId;
    teacher_full_name?: string;
    teacher_email?: string;
    teacher_phone?: string;
    is_primary: boolean;
    is_active: boolean;
    notes?: string;
    starts_at?: IsoDateString | null;
    ends_at?: IsoDateString | null;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface JoinRequestDto {
    id: JoinRequestId;
    request_type: JoinRequestTypeApi;
    status: JoinRequestStatusApi;
    user: UserShortDto;
    target_user: UserShortDto | null;
    organization: OrganizationShortDto | null;
    department: DepartmentShortDto | null;
    group: StudyGroupShortDto | null;
    message: string;
    review_comment: string;
    reviewed_by: UserShortDto | null;
    reviewed_at: IsoDateTimeString | null;
    expires_at: IsoDateTimeString | null;
    created_at: IsoDateTimeString;
    updated_at: IsoDateTimeString;
}

export interface OrganizationWritePayload {
    name?: string;
    short_name?: string;
    slug?: string;
    code?: string;
    description?: string;
    city?: string;
    address?: string;
    phone?: string;
    email?: string;
    website?: string;
    is_public?: boolean;
    is_default_public?: boolean;
}

export interface DepartmentWritePayload {
    organization_id?: OrganizationId;
    name?: string;
    short_name?: string;
    code?: string;
    description?: string;
}

export interface StudyGroupWritePayload {
    organization_id?: OrganizationId;
    department_id?: DepartmentId | null;
    name?: string;
    code?: string;
    description?: string;
    admission_year?: number | null;
    graduation_year?: number | null;
    course_number?: number | null;
    study_form?: StudyFormApi;
    status?: StudyGroupStatusApi;
}

export interface SubjectWritePayload {
    name?: string;
    short_name?: string;
    code?: string;
    description?: string;
}

export interface TeacherOrganizationWritePayload {
    teacher_id?: UserId;
    organization_id?: OrganizationId;
    position?: string;
    employment_type?: TeacherEmploymentTypeApi;
    is_primary?: boolean;
    is_active?: boolean;
    notes?: string;
    starts_at?: IsoDateString | null;
    ends_at?: IsoDateString | null;
}

export interface TeacherSubjectWritePayload {
    teacher_id?: UserId;
    subject_id?: SubjectId;
    is_primary?: boolean;
    is_active?: boolean;
    notes?: string;
}

export interface GroupCuratorWritePayload {
    group_id?: StudyGroupId;
    teacher_id?: UserId;
    is_primary?: boolean;
    is_active?: boolean;
    notes?: string;
    starts_at?: IsoDateString | null;
    ends_at?: IsoDateString | null;
}

export interface CodeSetPayload {
    raw_code?: string;
    expires_at?: IsoDateTimeString | null;
}

export interface TeacherRegistrationCodeResponse {
    organization: OrganizationDto;
    raw_code: string;
}

export interface GroupJoinCodeResponse {
    group: StudyGroupDto;
    raw_code: string;
}

export interface JoinRequestReviewPayload {
    comment?: string;
}

export interface ApiFieldErrors {
    [field: string]: string[] | string;
}

export interface ApiErrorResponse {
    detail?: string;
    error?: {
        code?: string;
        message?: string;
        fields?: ApiFieldErrors;
    };
}
