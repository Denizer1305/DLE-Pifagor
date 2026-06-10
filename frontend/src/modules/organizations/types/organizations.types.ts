import type {
    DepartmentDto,
    DepartmentId,
    GroupCuratorDto,
    JoinRequestDto,
    JoinRequestStatusApi,
    JoinRequestTypeApi,
    OrganizationDto,
    OrganizationId,
    SubjectDto,
    TeacherOrganizationDto,
    TeacherSubjectDto,
    StudyGroupDto,
} from "./organizations-api.types";
import type {
    DepartmentListItemView,
    EmptyStateView,
    GroupCuratorListItemView,
    JoinRequestListItemView,
    OrganizationEntityKey,
    OrganizationListItemView,
    OrganizationNavigationItem,
    OrganizationPageHeaderView,
    OrganizationSummaryCardView,
    StudyGroupListItemView,
    SubjectListItemView,
    TeacherOrganizationListItemView,
    TeacherSubjectListItemView,
} from "./organizations-view.types";
import type {
    OrganizationPaginationState,
    OrganizationTableConfig,
    OrganizationTableState,
} from "./organizations-table.types";

export interface OrganizationModuleDictionaries {
    organizations: OrganizationDto[];
    departments: DepartmentDictionaryItem[];
    studyGroups: StudyGroupDictionaryItem[];
    subjects: SubjectDto[];
    teachers: TeacherDictionaryItem[];
}

export interface DepartmentDictionaryItem {
    id: DepartmentId;
    organizationId: OrganizationId;
    name: string;
    shortName: string;
    code: string;
}

export interface StudyGroupDictionaryItem {
    id: number;
    organizationId: OrganizationId;
    departmentId: DepartmentId | null;
    name: string;
    code: string;
}

export interface TeacherDictionaryItem {
    id: number;
    fullName: string;
    email: string;
    phone: string;
}

export interface OrganizationPageScaffold {
    entity: OrganizationEntityKey;
    header: OrganizationPageHeaderView;
    navigation: OrganizationNavigationItem[];
    summary: OrganizationSummaryCardView[];
    table: OrganizationTableConfig;
    emptyState: EmptyStateView;
}

export interface OrganizationEntityPageState<TDto, TView> {
    items: TDto[];
    viewItems: TView[];
    tableState: OrganizationTableState;
    pagination: OrganizationPaginationState;
    filters: OrganizationFiltersState;
    errorMessage: string;
}

export interface OrganizationFiltersState {
    search: string;
    organizationId: OrganizationId | null;
    departmentId: DepartmentId | null;
    groupId: number | null;
    subjectId: number | null;
    teacherId: number | null;
    status: string;
    isActive: boolean | null;
    isPrimary: boolean | null;
    isPublic: boolean | null;
}

export interface OrganizationWorkspaceState {
    activeEntity: OrganizationEntityKey;
    isLoading: boolean;
    errorMessage: string;
}

export interface OrganizationEntitiesMap {
    organizations: OrganizationDto;
    departments: DepartmentDto;
    studyGroups: StudyGroupDto;
    subjects: SubjectDto;
    teacherOrganizations: TeacherOrganizationDto;
    teacherSubjects: TeacherSubjectDto;
    groupCurators: GroupCuratorDto;
    joinRequests: JoinRequestDto;
}

export interface OrganizationViewItemsMap {
    organizations: OrganizationListItemView;
    departments: DepartmentListItemView;
    studyGroups: StudyGroupListItemView;
    subjects: SubjectListItemView;
    teacherOrganizations: TeacherOrganizationListItemView;
    teacherSubjects: TeacherSubjectListItemView;
    groupCurators: GroupCuratorListItemView;
    joinRequests: JoinRequestListItemView;
}

export interface JoinRequestReviewContext {
    id: number;
    type: JoinRequestTypeApi;
    status: JoinRequestStatusApi;
    title: string;
    text: string;
    action: "approve" | "reject";
}