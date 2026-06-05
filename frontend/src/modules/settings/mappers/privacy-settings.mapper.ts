import { getProfileVisibilityLabel } from "@/modules/settings/mappers/settings-labels.mapper";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import {
    createSettingsScaffold,
    type SettingsUserContext,
} from "@/modules/settings/mappers/settings-scaffold.mapper";
import type {
    PrivacySettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import type { LocaleCode } from "@/stores/locale.store";

export function mapPrivacySettingsToPageState(
    settings: PrivacySettingsDto,
    context: SettingsUserContext,
    locale: LocaleCode = "ru",
): SettingsPageState<PrivacySettingsDto> {
    return {
        scaffold: createSettingsScaffold(context, "private-settings-page", locale),
        hero: localizeSettingsContent({
            icon: "fas fa-user-lock",
            topline: "Приватность и доступ",
            title: "Управление личными данными в платформе",
            text: "Здесь пользователь определяет, какие сведения видны другим участникам образовательной среды и как обрабатывается профиль.",
            badges: [
                { icon: "fas fa-eye", label: "Видимость профиля" },
                { icon: "fas fa-address-book", label: "Контакты и связи" },
                { icon: "fas fa-file-shield", label: "Персональные данные" },
            ],
            summaryRows: [
                { label: "Публичный профиль", value: getProfileVisibilityLabel(settings.profile_visibility, locale) },
                {
                    label: "Контакты",
                    value: settings.show_email || settings.show_phone ? "Частично видны" : "Скрыты",
                },
                { label: "Ролевые данные", value: settings.show_role_profile ? "Видны" : "Скрыты" },
                { label: "Экспорт данных", value: settings.allow_data_export ? "Разрешён" : "Запрещён" },
            ],
        }, locale),
        settings,
    };
}
