import {
    fetchAdminUserDetail,
    fetchAdminUsers,
    patchAdminUser,
    postAdminUser,
    postAdminUserStatusAction,
} from "@/modules/admin/api/admin-users.api";
import {
    mapAdminUserCreatePayload,
    createAdminUserEditForm,
    mapAdminUserDetail,
    mapAdminUserEditPayload,
    mapAdminUsersList,
} from "@/modules/admin/mappers/admin-users.mapper";
import type {
    AdminUserDetailDto,
    AdminUserDetailModel,
    AdminUserCreateForm,
    AdminUserEditForm,
    AdminUserStatusAction,
    AdminUsersFilters,
    AdminUsersListModel,
} from "@/modules/admin/types/admin-users.types";

export async function getAdminUsersList(
    filters: AdminUsersFilters,
): Promise<AdminUsersListModel> {
    const response = await fetchAdminUsers(filters);

    return mapAdminUsersList(response, filters);
}

export async function getAdminUserDetail(
    userId: number,
): Promise<AdminUserDetailModel> {
    const user = await fetchAdminUserDetail(userId);

    return mapAdminUserDetail(user);
}

export async function getAdminUserForEdit(
    userId: number,
): Promise<{ user: AdminUserDetailDto; form: AdminUserEditForm; model: AdminUserDetailModel }> {
    const user = await fetchAdminUserDetail(userId);

    return {
        user,
        form: createAdminUserEditForm(user),
        model: mapAdminUserDetail(user),
    };
}

export async function createAdminUser(
    form: AdminUserCreateForm,
): Promise<AdminUserDetailModel> {
    const user = await postAdminUser(mapAdminUserCreatePayload(form));

    return mapAdminUserDetail(user);
}

export async function saveAdminUserEdit(
    userId: number,
    form: AdminUserEditForm,
    expectedUpdatedAt: string,
): Promise<AdminUserDetailModel> {
    const user = await patchAdminUser(
        userId,
        mapAdminUserEditPayload(form, expectedUpdatedAt),
    );

    return mapAdminUserDetail(user);
}

export async function updateAdminUserStatus(
    userId: number,
    action: AdminUserStatusAction,
    expectedUpdatedAt: string,
    reason = "",
): Promise<AdminUserDetailModel> {
    const user = await postAdminUserStatusAction(userId, action, {
        expected_updated_at: expectedUpdatedAt,
        reason,
    });

    return mapAdminUserDetail(user);
}
