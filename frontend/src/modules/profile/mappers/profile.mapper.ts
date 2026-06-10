import {
    mapCurrentProfileToContactsCard,
    mapCurrentProfileToHero,
    mapCurrentProfileToIdentityCard,
} from "@/modules/profile/mappers/profile-content.mapper";
import { mapCurrentProfileToRoleSection } from "@/modules/profile/mappers/profile-role.mapper";
import { mapCurrentProfileToScaffoldModel } from "@/modules/profile/mappers/profile-scaffold.mapper";
import type {
    CurrentProfileDto,
    ProfilePageModel,
} from "@/modules/profile/types/profile.types";

export { mapCurrentProfileToScaffoldModel } from "@/modules/profile/mappers/profile-scaffold.mapper";

export function mapCurrentProfileToPageModel(
    dto: CurrentProfileDto,
): ProfilePageModel {
    return {
        scaffold: mapCurrentProfileToScaffoldModel(dto),
        hero: mapCurrentProfileToHero(dto),
        identityCard: mapCurrentProfileToIdentityCard(dto),
        contactsCard: mapCurrentProfileToContactsCard(dto),
        roleSection: mapCurrentProfileToRoleSection(dto),
    };
}
