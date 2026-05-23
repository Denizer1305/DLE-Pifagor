export { fetchCurrentProfile } from "@/modules/profile/api/profile.api";

export {
    deleteCurrentProfileAvatar,
    fetchCurrentProfileForEdit,
    updateCurrentProfile,
    uploadCurrentProfileAvatar,
} from "@/modules/profile/api/profile-edit.api";

export { useProfilePage } from "@/modules/profile/composables/useProfilePage";
export { useProfileEditForm } from "@/modules/profile/composables/useProfileEditForm";
export { useProfileAchievements } from "@/modules/profile/composables/useProfileAchievements";

export { createProfileNavigation } from "@/modules/profile/data/profile-navigation.data";

export {
    mapCurrentProfileToPageModel,
    mapCurrentProfileToScaffoldModel,
} from "@/modules/profile/mappers/profile.mapper";

export {
    mapCurrentProfileToEditForm,
    mapEditFormToPayload,
} from "@/modules/profile/mappers/profile-edit.mapper";

export { getProfilePage } from "@/modules/profile/services/profile.service";

export {
    getProfileEditPage,
    removeProfileAvatar,
    saveProfileAvatar,
    saveProfileEdit,
} from "@/modules/profile/services/profile-edit.service";

export type {
    CurrentProfileContactsDto,
    CurrentProfileDisplaySettingsDto,
    CurrentProfileDto,
    CurrentProfileIdentityDto,
    CurrentProfileRoleDto,
    ProfileContactsCardModel,
    ProfileHeroModel,
    ProfileIdentityCardModel,
    ProfileIdentityModel,
    ProfilePageModel,
    ProfileRoleCode,
    ProfileRoleModel,
    ProfileRoleSectionModel,
} from "@/modules/profile/types/profile.types";

export type {
    CurrentProfileEditPayload,
    ProfileEditFormErrors,
    ProfileEditFormState,
    ProfileEditPageState,
} from "@/modules/profile/types/profile-edit.types";