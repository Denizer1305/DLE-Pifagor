import {
    deleteCurrentProfileAvatar,
    fetchCurrentProfileForEdit,
    fetchProfileCitySuggestions,
    updateCurrentProfile,
    uploadCurrentProfileAvatar,
} from "@/modules/profile/api/profile-edit.api";
import {
    mapCurrentProfileToEditForm,
    mapProfileCitySuggestions,
} from "@/modules/profile/mappers/profile-edit.mapper";
import { mapCurrentProfileToPageModel } from "@/modules/profile/mappers/profile.mapper";
import type { ProfileEditFormState } from "@/modules/profile/types/profile-edit.types";
import type { ProfileCitySuggestion } from "@/modules/profile/types/profile-edit.types";
import type {
    CurrentProfileDto,
    ProfilePageModel,
} from "@/modules/profile/types/profile.types";

export interface ProfileEditServiceResult {
    source: CurrentProfileDto;
    form: ProfileEditFormState;
    pageModel: ProfilePageModel;
}

export async function getProfileEditPage(): Promise<ProfileEditServiceResult> {
    const source = await fetchCurrentProfileForEdit();

    return {
        source,
        form: mapCurrentProfileToEditForm(source),
        pageModel: mapCurrentProfileToPageModel(source),
    };
}

export async function saveProfileEdit(
    payload: Parameters<typeof updateCurrentProfile>[0],
): Promise<ProfileEditServiceResult> {
    const source = await updateCurrentProfile(payload);

    return {
        source,
        form: mapCurrentProfileToEditForm(source),
        pageModel: mapCurrentProfileToPageModel(source),
    };
}

export async function saveProfileAvatar(file: File): Promise<ProfileEditServiceResult> {
    const source = await uploadCurrentProfileAvatar(file);

    return {
        source,
        form: mapCurrentProfileToEditForm(source),
        pageModel: mapCurrentProfileToPageModel(source),
    };
}

export async function removeProfileAvatar(): Promise<ProfileEditServiceResult> {
    const source = await deleteCurrentProfileAvatar();

    return {
        source,
        form: mapCurrentProfileToEditForm(source),
        pageModel: mapCurrentProfileToPageModel(source),
    };
}

export async function getProfileCitySuggestions(
    query: string,
): Promise<ProfileCitySuggestion[]> {
    return mapProfileCitySuggestions(await fetchProfileCitySuggestions(query));
}
