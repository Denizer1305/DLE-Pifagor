import { getRoleLabel } from "@/modules/settings/mappers/settings-labels.mapper";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import {
    createSettingsScaffold,
    type SettingsUserContext,
} from "@/modules/settings/mappers/settings-scaffold.mapper";
import type {
    RoleSettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import type { LocaleCode } from "@/stores/locale.store";

export function mapRoleSettingsToPageState(
    settings: RoleSettingsDto,
    context: SettingsUserContext,
    locale: LocaleCode = "ru",
): SettingsPageState<RoleSettingsDto> {
    return {
        scaffold: createSettingsScaffold(context, "role-settings-page", locale),
        hero: localizeSettingsContent({
            icon: "fas fa-user-gear",
            topline: "Ролевые настройки",
            title: "Управление поведением кабинета по роли",
            text: "Здесь можно определить, какие блоки, действия, панели и подсказки будут отображаться для конкретной роли в платформе.",
            badges: [
                { icon: "fas fa-chalkboard-user", label: "Преподаватель" },
                { icon: "fas fa-user-graduate", label: "Студент" },
                { icon: "fas fa-people-roof", label: "Родитель" },
                { icon: "fas fa-user-shield", label: "Администратор" },
            ],
            summaryRows: [
                { label: "Активная роль", value: getRoleLabel(settings.active_role, locale) },
                { label: "Главный дашборд", value: "Персональный" },
                { label: "Быстрые действия", value: "Настраиваются" },
                { label: "AI-помощник", value: "По роли" },
            ],
        }, locale),
        settings,
    };
}
