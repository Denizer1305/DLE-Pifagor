import type {
    DepartmentId,
    GroupCuratorId,
    JoinRequestId,
    JoinRequestStatusApi,
    JoinRequestTypeApi,
    OrganizationId,
    StudyGroupId,
    StudyGroupStatusApi,
    SubjectId,
    TeacherOrganizationId,
    TeacherSubjectId,
    UserId,
} from "./organizations-api.types";

export type OrganizationEntityKey =
    | "organizations"
    | "departments"
    | "studyGroups"
    | "subjects"
    | "teacherOrganizations"
    | "teacherSubjects"
    | "groupCurators"
    | "joinRequests";

export type StatusTone =
    | "neutral"
    | "accent"
    | "success"
    | "warning"
    | "danger"
    | "muted";

export interface OrganizationNavigationItem {
    key: OrganizationEntityKey;
    label: string;
    hint: string;
    routeName: string;
    icon: string;
    badge?: number | string;
}

export interface OrganizationPageHeaderView {
    eyebrow: string;
    title: string;
    description: string;
    primaryActionLabel?: string;
    secondaryActionLabel?: string;
}

export interface OrganizationSummaryCardView {
    key: string;
    label: string;
    value: string;
    meta: string;
    icon: string;
    tone: StatusTone;
    trend?: {
        label: string;
        tone: StatusTone;
    };
}

export interface StatusBadgeView {
    label: string;
    tone: StatusTone;
    className: string;
}

export interface OrganizationListItemView {
    id: OrganizationId;
    title: string;
    subtitle: string;
    code: string;
    city: string;
    email: string;
    phone: string;
    website: string;
    logoUrl: string | null;
    isActive: boolean;
    isPublic: boolean;
    isDefaultPublic: boolean;
    status: StatusBadgeView;
    meta: string[];
}

export interface DepartmentListItemView {
    id: DepartmentId;
    title: string;
    subtitle: string;
    code: string;
    organizationTitle: string;
    isActive: boolean;
    status: StatusBadgeView;
    meta: string[];
}

export interface StudyGroupListItemView {
    id: StudyGroupId;
    title: string;
    subtitle: string;
    code: string;
    organizationTitle: string;
    departmentTitle: string;
    admissionYear: string;
    graduationYear: string;
    courseNumber: string;
    statusCode: StudyGroupStatusApi;
    status: StatusBadgeView;
    isActive: boolean;
    isArchived: boolean;
    meta: string[];
}

export interface SubjectListItemView {
    id: SubjectId;
    title: string;
    subtitle: string;
    code: string;
    isActive: boolean;
    status: StatusBadgeView;
    meta: string[];
}

export interface TeacherOrganizationListItemView {
    id: TeacherOrganizationId;
    teacherId: UserId;
    teacherName: string;
    teacherEmail: string;
    teacherPhone: string;
    organizationTitle: string;
    position: string;
    employmentTypeLabel: string;
    isPrimary: boolean;
    isActive: boolean;
    status: StatusBadgeView;
    meta: string[];
}

export interface TeacherSubjectListItemView {
    id: TeacherSubjectId;
    teacherId: UserId;
    teacherName: string;
    teacherEmail: string;
    teacherPhone: string;
    subjectTitle: string;
    subjectCode: string;
    isPrimary: boolean;
    isActive: boolean;
    status: StatusBadgeView;
    meta: string[];
}

export interface GroupCuratorListItemView {
    id: GroupCuratorId;
    teacherId: UserId;
    teacherName: string;
    teacherEmail: string;
    teacherPhone: string;
    groupTitle: string;
    isPrimary: boolean;
    isActive: boolean;
    status: StatusBadgeView;
    meta: string[];
}

export interface JoinRequestListItemView {
    id: JoinRequestId;
    type: JoinRequestTypeApi;
    typeLabel: string;
    statusCode: JoinRequestStatusApi;
    status: StatusBadgeView;
    userName: string;
    userContacts: string;
    targetTitle: string;
    message: string;
    reviewComment: string;
    createdAtLabel: string;
    reviewedAtLabel: string;
    canReview: boolean;
    meta: string[];
}

export interface OrganizationDetailsView {
    title: string;
    subtitle: string;
    eyebrow: string;
    status: StatusBadgeView;
    rows: OrganizationDetailsRow[];
    chips: string[];
}

export interface OrganizationDetailsRow {
    label: string;
    value: string;
    href?: string;
}

export interface EmptyStateView {
    icon: string;
    title: string;
    text: string;
    actionLabel?: string;
}