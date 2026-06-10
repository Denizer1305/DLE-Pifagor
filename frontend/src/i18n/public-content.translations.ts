import { authContentPrimaryTranslations } from "@/i18n/auth-content-primary.translations";
import { authContentSecondaryTranslations } from "@/i18n/auth-content-secondary.translations";
import { publicAboutTranslations } from "@/i18n/public-about.translations";
import { publicContactsTeachersExtraTranslations } from "@/i18n/public-contacts-teachers-extra.translations";
import { publicContactsTeachersInitialTranslations } from "@/i18n/public-contacts-teachers-initial.translations";
import { publicHomeExtraTranslations } from "@/i18n/public-home-extra.translations";
import { publicHomeInitialTranslations } from "@/i18n/public-home-initial.translations";

export const publicContentTranslations: Record<string, string> = {
    ...publicHomeInitialTranslations,
    ...publicContactsTeachersInitialTranslations,
    ...authContentPrimaryTranslations,
    ...authContentSecondaryTranslations,
    ...publicContactsTeachersExtraTranslations,
    ...publicHomeExtraTranslations,
    ...publicAboutTranslations,
};
