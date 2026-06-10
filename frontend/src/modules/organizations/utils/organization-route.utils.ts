import type {
    DepartmentId,
    GroupCuratorId,
    JoinRequestId,
    OrganizationEntityKey,
    OrganizationId,
    StudyGroupId,
    SubjectId,
    TeacherOrganizationId,
    TeacherSubjectId,
} from "../types";

const DEFAULT_ORGANIZATION_ROUTE_NAME = "admin-organizations";

export const ORGANIZATION_ROUTE_NAMES: Record<OrganizationEntityKey, string> = {
    organizations: DEFAULT_ORGANIZATION_ROUTE_NAME,
    departments: "admin-organization-departments",
    studyGroups: "admin-organization-study-groups",
    subjects: "admin-organization-subjects",
    teacherOrganizations: "admin-organization-teachers",
    teacherSubjects: "admin-organization-teacher-subjects",
    groupCurators: "admin-organization-group-curators",
    joinRequests: "admin-organization-join-requests",
};

export type OrganizationRouteEntityId =
    | OrganizationId
    | DepartmentId
    | StudyGroupId
    | SubjectId
    | TeacherOrganizationId
    | TeacherSubjectId
    | GroupCuratorId
    | JoinRequestId;

export interface OrganizationRouteLocation {
    name: string;
    params?: Record<string, string | number>;
    query?: Record<string, string | number | boolean | null | undefined>;
}

export function getOrganizationEntityRouteName(
    entity: OrganizationEntityKey,
): string {
    return ORGANIZATION_ROUTE_NAMES[entity] ?? DEFAULT_ORGANIZATION_ROUTE_NAME;
}

export function createOrganizationEntityRoute(
    entity: OrganizationEntityKey,
): OrganizationRouteLocation {
    return {
        name: getOrganizationEntityRouteName(entity),
    };
}

export function createOrganizationEntityDetailRoute(
    entity: OrganizationEntityKey,
    id: OrganizationRouteEntityId,
): OrganizationRouteLocation {
    return {
        name: getOrganizationEntityRouteName(entity),
        query: {
            selected: id,
        },
    };
}

export function createOrganizationEntityCreateRoute(
    entity: OrganizationEntityKey,
): OrganizationRouteLocation {
    return {
        name: getOrganizationEntityRouteName(entity),
        query: {
            action: "create",
        },
    };
}

export function createOrganizationEntityEditRoute(
    entity: OrganizationEntityKey,
    id: OrganizationRouteEntityId,
): OrganizationRouteLocation {
    return {
        name: getOrganizationEntityRouteName(entity),
        query: {
            action: "edit",
            selected: id,
        },
    };
}
