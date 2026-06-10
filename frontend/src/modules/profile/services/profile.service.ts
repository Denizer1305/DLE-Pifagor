import { fetchCurrentProfile } from "@/modules/profile/api/profile.api";
import { mapCurrentProfileToPageModel } from "@/modules/profile/mappers/profile.mapper";
import type {
    CurrentProfileDto,
    ProfilePageModel,
} from "@/modules/profile/types/profile.types";

export interface ProfilePageServiceResult {
    source: CurrentProfileDto;
    pageModel: ProfilePageModel;
}

export async function getProfilePage(): Promise<ProfilePageServiceResult> {
    const source = await fetchCurrentProfile();

    return {
        source,
        pageModel: mapCurrentProfileToPageModel(source),
    };
}
