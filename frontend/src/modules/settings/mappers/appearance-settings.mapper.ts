import {
    getColorModeLabel,
    getDensityLabel,
    getLanguageLabel,
    getThemeLabel,
} from "@/modules/settings/mappers/settings-labels.mapper";
import {
    createSettingsScaffold,
    type SettingsUserContext,
} from "@/modules/settings/mappers/settings-scaffold.mapper";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import type {
    AppearanceSettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import type { LocaleCode } from "@/stores/locale.store";

export function mapAppearanceSettingsToPageState(
    settings: AppearanceSettingsDto,
    context: SettingsUserContext,
    locale: LocaleCode = "ru",
): SettingsPageState<AppearanceSettingsDto> {
    return {
        scaffold: createSettingsScaffold(context, "appearance-settings-page", locale),
        hero: localizeSettingsContent({
            icon: "fas fa-palette",
            topline: "Внешний вид и интерфейс",
            title: "Настройте платформу под свой стиль работы",
            text: "Здесь можно выбрать цветовую схему, режим интерфейса, плотность отображения, анимации, карточки и другие визуальные параметры кабинета.",
            badges: [
                { icon: "fas fa-fill-drip", label: "10 цветовых схем" },
                { icon: "fas fa-moon", label: "Светлый / тёмный / системный режим" },
                { icon: "fas fa-sliders", label: "Гибкая настройка интерфейса" },
            ],
            summaryRows: [
                { label: "Тема", value: getThemeLabel(settings.theme, locale) },
                { label: "Режим", value: getColorModeLabel(settings.color_mode, locale) },
                { label: "Язык", value: getLanguageLabel(settings.language, locale) },
                { label: "Плотность", value: getDensityLabel(settings.density, locale) },
                { label: "Анимации", value: settings.animations_enabled ? "Включены" : "Выключены" },
            ],
        }, locale),
        settings,
    };
}
