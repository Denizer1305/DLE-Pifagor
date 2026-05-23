import { httpClient } from "@/services/api/http.client";
import type {
    CurrentProfileEditPayload,
    ProfileCitySuggestionDto,
} from "@/modules/profile/types/profile-edit.types";
import type { CurrentProfileDto } from "@/modules/profile/types/profile.types";

const CURRENT_PROFILE_EDIT_URL = "/users/profiles/me/edit/";
const CURRENT_PROFILE_AVATAR_URL = "/users/profiles/me/avatar/";
const CURRENT_PROFILE_CITY_SUGGESTIONS_URL = "/users/profiles/me/city-suggestions/";

export async function fetchCurrentProfileForEdit(): Promise<CurrentProfileDto> {
    const response = await httpClient.get<CurrentProfileDto>(CURRENT_PROFILE_EDIT_URL);

    return response.data;
}

export async function updateCurrentProfile(
    payload: CurrentProfileEditPayload,
): Promise<CurrentProfileDto> {
    const response = await httpClient.patch<CurrentProfileDto>(
        CURRENT_PROFILE_EDIT_URL,
        payload,
    );

    return response.data;
}

export async function uploadCurrentProfileAvatar(file: File): Promise<CurrentProfileDto> {
    const formData = new FormData();

    formData.append("avatar", file);

    const response = await httpClient.post<CurrentProfileDto>(
        CURRENT_PROFILE_AVATAR_URL,
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        },
    );

    return response.data;
}

export async function deleteCurrentProfileAvatar(): Promise<CurrentProfileDto> {
    const response = await httpClient.delete<CurrentProfileDto>(
        CURRENT_PROFILE_AVATAR_URL,
    );

    return response.data;
}

export async function fetchProfileCitySuggestions(
    query: string,
): Promise<ProfileCitySuggestionDto[]> {
    const response = await httpClient.get<{ suggestions: ProfileCitySuggestionDto[] }>(
        CURRENT_PROFILE_CITY_SUGGESTIONS_URL,
        {
            params: { query },
        },
    );

    return response.data.suggestions;
}
