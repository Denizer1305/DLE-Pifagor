export {
    changePassword,
    fetchAppearanceSettings,
    fetchNotificationSettings,
    fetchPrivacySettings,
    fetchRoleSettings,
    fetchSecuritySessions,
    fetchSecuritySettings,
    fetchUserSettings,
    logoutAllSecuritySessions,
    logoutSecuritySession,
    updateAppearanceSettings,
    updateNotificationSettings,
    updatePrivacySettings,
    updateRoleSettings,
    updateSecuritySettings,
    updateUserSettings,
} from "@/modules/settings/api/settings.api";

export { useAppearanceSettings } from "@/modules/settings/composables/useAppearanceSettings";
export { useNotificationSettings } from "@/modules/settings/composables/useNotificationSettings";
export { usePrivacySettings } from "@/modules/settings/composables/usePrivacySettings";
export { useRoleSettings } from "@/modules/settings/composables/useRoleSettings";
export { useSecuritySettings } from "@/modules/settings/composables/useSecuritySettings";
export { useSettingsPage } from "@/modules/settings/composables/useSettingsPage";

export { appearanceThemes } from "@/modules/settings/data/appearance-themes.data";
export {
    appearancePageContent,
    settingsCenterPageContent,
} from "@/modules/settings/data/appearance-page.data";
export {
    adminRoleOptions,
    guardianRoleOptions,
    learnerRoleOptions,
    settingsRoleOptions,
    settingsRoleTitles,
    teacherRoleOptions,
} from "@/modules/settings/data/role-settings.data";
export { settingsCenterCards } from "@/modules/settings/data/settings-center.data";
export { createSettingsNavigation } from "@/modules/settings/data/settings-navigation.data";
export {
    colorModeOptions,
    densityOptions,
    languageOptions,
    notificationFrequencyOptions,
    profileVisibilityOptions,
    sessionLifetimeOptions,
} from "@/modules/settings/data/settings-options.data";
export { securityPasswordFormContent } from "@/modules/settings/data/security-settings.data";
export {
    getSettingsLocaleLabel,
    localizeSettingsContent,
    translateSettingsText,
} from "@/modules/settings/data/settings-translations.data";

export {
    createSettingsScaffold,
    mapAppearanceSettingsToPageState,
    mapNotificationSettingsToPageState,
    mapPrivacySettingsToPageState,
    mapRoleSettingsToPageState,
    mapSecuritySettingsToPageState,
    mapUserSettingsToCenterModel,
} from "@/modules/settings/mappers/settings.mapper";

export {
    getAppearanceSettings,
    getNotificationSettings,
    getPrivacySettings,
    getRoleSettings,
    getSecuritySessions,
    getSecuritySettings,
    getUserSettings,
    logoutAllSessions,
    logoutSession,
    saveAppearanceSettings,
    saveNotificationSettings,
    savePassword,
    savePrivacySettings,
    saveRoleSettings,
    saveSecuritySettings,
    saveUserSettings,
} from "@/modules/settings/services/settings.service";

export type {
    AdminRoleSettingsDto,
    AppearanceSettingsDto,
    AppearanceThemeModel,
    ChangePasswordPayload,
    GuardianRoleSettingsDto,
    LearnerRoleSettingsDto,
    NotificationFrequency,
    NotificationSettingsDto,
    PasswordFormErrors,
    PasswordFormState,
    PrivacySettingsDto,
    ProfileVisibility,
    RoleSettingsDto,
    SecuritySessionDto,
    SecuritySessionsDto,
    SecuritySettingsDto,
    SessionLifetimeMode,
    SettingsCenterCardModel,
    SettingsCenterModel,
    SettingsColorMode,
    SettingsDensity,
    SettingsLanguage,
    SettingsHeroModel,
    SettingsPageState,
    SettingsPasswordFieldModel,
    SettingsPasswordFormContent,
    SettingsRoleCode,
    SettingsSelectOptionModel,
    SettingsTheme,
    SettingsToggleItemModel,
    TeacherRoleSettingsDto,
    UserSettingsDto,
} from "@/modules/settings/types/settings.types";
