import type { RouteLocationNormalizedLoaded, Router } from "vue-router";

import { ROLE_CODES, type RoleCode } from "@/app/constants/roles.constants";

const SAFE_INTERNAL_PATH_PATTERN = /^\/(?!\/)/;

export interface DashboardRedirectContext {
    roleCode?: RoleCode | "" | null;
    isSuperuser?: boolean;
}

export function isSafeRedirectPath(value: unknown): value is string {
    if (typeof value !== "string") {
        return false;
    }

    if (!value.trim()) {
        return false;
    }

    return SAFE_INTERNAL_PATH_PATTERN.test(value);
}

export function getRedirectPathFromRoute(
    route: RouteLocationNormalizedLoaded,
    fallbackPath = "/student",
): string {
    const redirect = route.query.redirect;

    if (isSafeRedirectPath(redirect)) {
        return redirect;
    }

    return fallbackPath;
}

export function isAdminRole(roleCode: RoleCode | "" | null | undefined): boolean {
    return (
        roleCode === ROLE_CODES.DIRECTOR ||
        roleCode === ROLE_CODES.ORG_ADMIN ||
        roleCode === ROLE_CODES.DEPARTMENT_HEAD ||
        roleCode === ROLE_CODES.SUPERADMIN ||
        roleCode === ROLE_CODES.PLATFORM_ADMIN ||
        roleCode === ROLE_CODES.ADMIN
    );
}

export function isTeacherRole(roleCode: RoleCode | "" | null | undefined): boolean {
    return (
        roleCode === ROLE_CODES.TEACHER ||
        roleCode === ROLE_CODES.CURATOR ||
        roleCode === ROLE_CODES.METHODIST ||
        roleCode === ROLE_CODES.ORGANIZER ||
        roleCode === ROLE_CODES.MENTOR
    );
}

export function getDashboardPathByRole(
    roleCode: RoleCode | "" | null | undefined,
    isSuperuser = false,
): string {
    if (isSuperuser || isAdminRole(roleCode)) {
        return "/admin";
    }

    if (isTeacherRole(roleCode)) {
        return "/teacher";
    }

    if (roleCode === ROLE_CODES.GUARDIAN) {
        return "/parent";
    }

    return "/student";
}

export function getDashboardRouteNameByRole(
    roleCode: RoleCode | "" | null | undefined,
    isSuperuser = false,
): string {
    if (isSuperuser || isAdminRole(roleCode)) {
        return "admin-dashboard";
    }

    if (isTeacherRole(roleCode)) {
        return "teacher-dashboard";
    }

    if (roleCode === ROLE_CODES.GUARDIAN) {
        return "parent-dashboard";
    }

    return "student-dashboard";
}

export function getDashboardPathByContext(context: DashboardRedirectContext): string {
    return getDashboardPathByRole(
        context.roleCode,
        Boolean(context.isSuperuser),
    );
}

export function getDashboardRouteNameByContext(context: DashboardRedirectContext): string {
    return getDashboardRouteNameByRole(
        context.roleCode,
        Boolean(context.isSuperuser),
    );
}

export async function redirectAfterLogin(
    router: Router,
    route: RouteLocationNormalizedLoaded,
    roleCode: RoleCode | "" | null | undefined,
    isSuperuser = false,
): Promise<void> {
    const fallbackPath = getDashboardPathByRole(roleCode, isSuperuser);
    if (isSuperuser || isAdminRole(roleCode)) {
        await router.push(fallbackPath);
        return;
    }

    const redirectPath = getRedirectPathFromRoute(route, fallbackPath);

    await router.push(redirectPath);
}

export async function redirectToLogin(
    router: Router,
    redirectPath?: string,
): Promise<void> {
    await router.push({
        name: "login",
        query: redirectPath
            ? {
                redirect: redirectPath,
            }
            : undefined,
    });
}

export async function redirectAfterLogout(router: Router): Promise<void> {
    await router.push({
        name: "login",
    });
}

export async function redirectAfterRegistration(router: Router): Promise<void> {
    await router.push({
        name: "login",
    });
}
