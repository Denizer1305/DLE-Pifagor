import { settingsCenterCards } from "@/modules/settings/data/settings-center.data";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import {
    getColorModeLabel,
    getProfileVisibilityLabel,
    getThemeLabel,
} from "@/modules/settings/mappers/settings-labels.mapper";
import {
    createSettingsScaffold,
    type SettingsUserContext,
} from "@/modules/settings/mappers/settings-scaffold.mapper";
import type {
    SettingsCenterModel,
    UserSettingsDto,
} from "@/modules/settings/types/settings.types";
import type { LocaleCode } from "@/stores/locale.store";

export function mapUserSettingsToCenterModel(
    settings: UserSettingsDto,
    context: SettingsUserContext,
    locale: LocaleCode = "ru",
): SettingsCenterModel {
    return {
        scaffold: createSettingsScaffold(context, "settings-page", locale),
        hero: localizeSettingsContent({
            icon: "fas fa-sliders",
            topline: "Центр настроек",
            title: "Управление аккаунтом и платформой",
            text: "Здесь собраны основные параметры аккаунта: безопасность, уведомления, внешний вид, приватность и рабочие настройки, связанные с ролью пользователя.",
            badges: [
                {
                    icon: "fas fa-envelope-circle-check",
                    label: settings.notifications.channels.email ? "Email включён" : "Email отключён",
                },
                {
                    icon: "fas fa-bell",
                    label: settings.notifications.channels.in_app ? "Уведомления активны" : "Уведомления выключены",
                },
                { icon: "fas fa-palette", label: getThemeLabel(settings.appearance.theme, locale) },
                { icon: "fas fa-user-tie", label: context.roleLabel },
            ],
            summaryRows: [
                { label: "Тема", value: getThemeLabel(settings.appearance.theme, locale) },
                { label: "Режим", value: getColorModeLabel(settings.appearance.color_mode, locale) },
                {
                    label: "Уведомления",
                    value: settings.notifications.channels.in_app ? "Включены" : "Выключены",
                },
                {
                    label: "Приватность",
                    value: getProfileVisibilityLabel(settings.privacy.profile_visibility, locale),
                },
            ],
        }, locale),
        cards: localizeSettingsContent(settingsCenterCards, locale),
    };
}
