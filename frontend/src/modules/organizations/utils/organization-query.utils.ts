import type {
    ApiListQuery,
    DepartmentListQuery,
    GroupCuratorListQuery,
    JoinRequestListQuery,
    JoinRequestStatusApi,
    OrganizationListQuery,
    StudyGroupListQuery,
    StudyGroupStatusApi,
    SubjectListQuery,
    TeacherOrganizationListQuery,
    TeacherSubjectListQuery,
} from "../types/organizations-api.types";
import type { OrganizationPaginationState } from "../types/organizations-table.types";
import type { OrganizationFiltersState } from "../types/organizations.types";

type QueryValue = string | number | boolean | null | undefined;

function isEmptyQueryValue(value: unknown): boolean {
    return value === undefined || value === null || value === "";
}

export function cleanQuery<TQuery extends object>(
    query: TQuery,
): Partial<TQuery> {
    const cleanedQuery: Partial<TQuery> = {};

    Object.entries(query).forEach(([key, value]) => {
        if (isEmptyQueryValue(value)) {
            return;
        }

        cleanedQuery[key as keyof TQuery] = value as TQuery[keyof TQuery];
    });

    return cleanedQuery;
}

export function createPaginationQuery(
    pagination?: Partial<OrganizationPaginationState>,
): ApiListQuery {
    if (!pagination) {
        return {};
    }

    return cleanQuery({
        page: pagination.page,
        page_size: pagination.pageSize,
    });
}

export function createBaseListQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): ApiListQuery {
    return cleanQuery({
        search: filters.search?.trim(),
        ...createPaginationQuery(pagination),
    });
}

export function createOrganizationsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): OrganizationListQuery {
    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        is_active: filters.isActive ?? undefined,
        is_public: filters.isPublic ?? undefined,
    });
}

export function createDepartmentsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): DepartmentListQuery {
    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        organization_id: filters.organizationId ?? undefined,
        is_active: filters.isActive ?? undefined,
    });
}

export function createStudyGroupsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): StudyGroupListQuery {
    const status = filters.status
        ? (filters.status as StudyGroupStatusApi)
        : undefined;

    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        organization_id: filters.organizationId ?? undefined,
        department_id: filters.departmentId ?? undefined,
        status,
        is_active: filters.isActive ?? undefined,
    });
}

export function createSubjectsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): SubjectListQuery {
    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        is_active: filters.isActive ?? undefined,
    });
}

export function createTeacherOrganizationsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): TeacherOrganizationListQuery {
    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        teacher_id: filters.teacherId ?? undefined,
        organization_id: filters.organizationId ?? undefined,
        is_active: filters.isActive ?? undefined,
        is_primary: filters.isPrimary ?? undefined,
    });
}

export function createTeacherSubjectsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): TeacherSubjectListQuery {
    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        teacher_id: filters.teacherId ?? undefined,
        subject_id: filters.subjectId ?? undefined,
        organization_id: filters.organizationId ?? undefined,
        is_active: filters.isActive ?? undefined,
        is_primary: filters.isPrimary ?? undefined,
    });
}

export function createGroupCuratorsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): GroupCuratorListQuery {
    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        teacher_id: filters.teacherId ?? undefined,
        group_id: filters.groupId ?? undefined,
        organization_id: filters.organizationId ?? undefined,
        is_active: filters.isActive ?? undefined,
        is_primary: filters.isPrimary ?? undefined,
    });
}

export function createJoinRequestsQuery(
    filters: Partial<OrganizationFiltersState>,
    pagination?: Partial<OrganizationPaginationState>,
): JoinRequestListQuery {
    const status = filters.status
        ? (filters.status as JoinRequestStatusApi)
        : undefined;

    return cleanQuery({
        ...createBaseListQuery(filters, pagination),
        status,
        organization_id: filters.organizationId ?? undefined,
        department_id: filters.departmentId ?? undefined,
        group_id: filters.groupId ?? undefined,
    });
}

export function toSearchParams(query: object): URLSearchParams {
    const params = new URLSearchParams();

    Object.entries(cleanQuery(query)).forEach(([key, value]) => {
        if (isEmptyQueryValue(value)) {
            return;
        }

        params.set(key, String(value as QueryValue));
    });

    return params;
}

export function getQueryString(query: object): string {
    const params = toSearchParams(query);
    const queryString = params.toString();

    return queryString ? `?${queryString}` : "";
}
