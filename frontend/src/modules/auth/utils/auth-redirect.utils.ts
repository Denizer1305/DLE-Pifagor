import type { RouteLocationNormalizedLoaded, Router } from "vue-router";

import { ROLE_CODES, type RoleCode } from "@/app/constants/roles.constants";

const SAFE_INTERNAL_PATH_PATTERN = /^\/(?!\/)/;

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

export function getDashboardPathByRole(roleCode: RoleCode | "" | null | undefined): string {
    if (
        roleCode === ROLE_CODES.TEACHER ||
        roleCode === ROLE_CODES.CURATOR ||
        roleCode === ROLE_CODES.METHODIST ||
        roleCode === ROLE_CODES.ORGANIZER ||
        roleCode === ROLE_CODES.MENTOR
    ) {
        return "/teacher";
    }

    if (roleCode === ROLE_CODES.GUARDIAN) {
        return "/parent";
    }

    if (
        roleCode === ROLE_CODES.DIRECTOR ||
        roleCode === ROLE_CODES.ORG_ADMIN ||
        roleCode === ROLE_CODES.DEPARTMENT_HEAD ||
        roleCode === ROLE_CODES.SUPERADMIN
    ) {
        return "/admin";
    }

    return "/student";
}

export function getDashboardRouteNameByRole(roleCode: RoleCode | "" | null | undefined): string {
    if (
        roleCode === ROLE_CODES.TEACHER ||
        roleCode === ROLE_CODES.CURATOR ||
        roleCode === ROLE_CODES.METHODIST ||
        roleCode === ROLE_CODES.ORGANIZER ||
        roleCode === ROLE_CODES.MENTOR
    ) {
        return "teacher-dashboard";
    }

    if (roleCode === ROLE_CODES.GUARDIAN) {
        return "parent-dashboard";
    }

    if (
        roleCode === ROLE_CODES.DIRECTOR ||
        roleCode === ROLE_CODES.ORG_ADMIN ||
        roleCode === ROLE_CODES.DEPARTMENT_HEAD ||
        roleCode === ROLE_CODES.SUPERADMIN
    ) {
        return "admin-dashboard";
    }

    return "student-dashboard";
}

export async function redirectAfterLogin(
    router: Router,
    route: RouteLocationNormalizedLoaded,
    roleCode: RoleCode | "" | null | undefined,
): Promise<void> {
    const fallbackPath = getDashboardPathByRole(roleCode);
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
