import { httpClient } from "@/services/api/http.client";
import type { UserDetail, UserUpdatePayload } from "@/modules/users/types/user.types";

const USERS_BASE_URL = "/users/users";

export async function getCurrentUser(): Promise<UserDetail> {
    const response = await httpClient.get<UserDetail>(`${USERS_BASE_URL}/me/`);

    return response.data;
}

export async function getUserById(id: number): Promise<UserDetail> {
    const response = await httpClient.get<UserDetail>(`${USERS_BASE_URL}/${id}/`);

    return response.data;
}

export async function updateUser(id: number, payload: UserUpdatePayload): Promise<UserDetail> {
    const response = await httpClient.patch<UserDetail>(`${USERS_BASE_URL}/${id}/`, payload);

    return response.data;
}