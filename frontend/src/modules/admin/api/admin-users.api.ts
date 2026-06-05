import { httpClient } from "@/services/api/http.client";
import type {
    AdminUserDetailDto,
    AdminUsersPaginatedDto,
    AdminUserStatusAction,
    AdminUserUpdatePayload,
    AdminUsersFilters,
} from "@/modules/admin/types/admin-users.types";

const ADMIN_USERS_URL = "/users/admin/users/";

export async function fetchAdminUsers(
    filters: AdminUsersFilters,
): Promise<AdminUsersPaginatedDto> {
    const response = await httpClient.get<AdminUsersPaginatedDto>(
        ADMIN_USERS_URL,
        {
            params: {
                page: filters.page,
                page_size: filters.pageSize,
                role_group: filters.roleGroup || undefined,
                search: filters.search || undefined,
                status: filters.status || undefined,
                ordering: filters.ordering || undefined,
            },
        },
    );

    return response.data;
}

export async function fetchAdminUserDetail(userId: number): Promise<AdminUserDetailDto> {
    const response = await httpClient.get<AdminUserDetailDto>(`${ADMIN_USERS_URL}${userId}/`);

    return response.data;
}

export async function patchAdminUser(
    userId: number,
    payload: AdminUserUpdatePayload,
): Promise<AdminUserDetailDto> {
    const response = await httpClient.patch<AdminUserDetailDto>(
        `${ADMIN_USERS_URL}${userId}/`,
        payload,
    );

    return response.data;
}

export async function postAdminUserStatusAction(
    userId: number,
    action: AdminUserStatusAction,
    payload: Pick<AdminUserUpdatePayload, "expected_updated_at" | "reason">,
): Promise<AdminUserDetailDto> {
    const response = await httpClient.post<AdminUserDetailDto>(
        `${ADMIN_USERS_URL}${userId}/${action}/`,
        payload,
    );

    return response.data;
}
