import { httpClient } from "@/services/api/http.client";
import type { CurrentProfileDto } from "@/modules/profile/types/profile.types";

const CURRENT_PROFILE_URL = "/users/profiles/me/";

export async function fetchCurrentProfile(): Promise<CurrentProfileDto> {
    const response = await httpClient.get<CurrentProfileDto>(CURRENT_PROFILE_URL);

    return response.data;
}