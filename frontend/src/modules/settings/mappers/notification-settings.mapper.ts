import { getFrequencyLabel } from "@/modules/settings/mappers/settings-labels.mapper";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import {
    createSettingsScaffold,
    type SettingsUserContext,
} from "@/modules/settings/mappers/settings-scaffold.mapper";
import type {
    NotificationSettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import type { LocaleCode } from "@/stores/locale.store";

export function mapNotificationSettingsToPageState(
    settings: NotificationSettingsDto,
    context: SettingsUserContext,
    locale: LocaleCode = "ru",
): SettingsPageState<NotificationSettingsDto> {
    return {
        scaffold: createSettingsScaffold(context, "notification-settings-page", locale),
        hero: localizeSettingsContent({
            icon: "fas fa-bell",
            topline: "Настройки уведомлений",
            title: "Управление сигналами, событиями и напоминаниями",
            text: "Здесь можно выбрать, какие уведомления приходят в интерфейс платформы, на электронную почту, в VK, MAX или по другим подключённым каналам.",
            badges: [
                {
                    icon: "fas fa-display",
                    label: settings.channels.in_app ? "Внутренние уведомления активны" : "Внутренние уведомления выключены",
                },
                { icon: "fas fa-envelope", label: settings.channels.email ? "Email включён" : "Email отключён" },
                { icon: "fab fa-vk", label: settings.channels.vk ? "VK подключён" : "VK отключён" },
                { icon: "fas fa-comment-dots", label: settings.channels.max ? "MAX подключён" : "MAX отключён" },
            ],
            summaryRows: [
                { label: "Учебные события", value: getFrequencyLabel(settings.frequency.education, locale) },
                { label: "Системные события", value: getFrequencyLabel(settings.frequency.system, locale) },
                { label: "Маркетинг", value: getFrequencyLabel(settings.frequency.marketing, locale) },
                { label: "Дайджест", value: settings.digest_time },
            ],
        }, locale),
        settings,
    };
}
