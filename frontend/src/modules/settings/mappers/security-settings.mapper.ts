import { getSessionLifetimeLabel } from "@/modules/settings/mappers/settings-labels.mapper";
import { localizeSettingsContent } from "@/modules/settings/data/settings-translations.data";
import {
    createSettingsScaffold,
    type SettingsUserContext,
} from "@/modules/settings/mappers/settings-scaffold.mapper";
import type {
    SecuritySettingsDto,
    SettingsPageState,
} from "@/modules/settings/types/settings.types";
import type { LocaleCode } from "@/stores/locale.store";

export function mapSecuritySettingsToPageState(
    settings: SecuritySettingsDto,
    context: SettingsUserContext,
    locale: LocaleCode = "ru",
): SettingsPageState<SecuritySettingsDto> {
    return {
        scaffold: createSettingsScaffold(context, "security-settings-page", locale),
        hero: localizeSettingsContent({
            icon: "fas fa-shield-halved",
            topline: "Настройки безопасности",
            title: "Защита аккаунта и контроль доступа",
            text: "Здесь можно управлять паролем, активными сессиями, подтверждением входов и дополнительными мерами защиты.",
            badges: [
                { icon: "fas fa-key", label: "Смена пароля" },
                { icon: "fas fa-mobile-screen", label: "Активные сессии" },
                {
                    icon: "fas fa-envelope-circle-check",
                    label: settings.login_notifications_enabled ? "Уведомления о входе включены" : "Уведомления о входе выключены",
                },
                {
                    icon: "fas fa-shield",
                    label: settings.two_factor_enabled ? "2FA включена" : "2FA выключена",
                },
            ],
            summaryRows: [
                {
                    label: "Уведомления о входе",
                    value: settings.login_notifications_enabled ? "Включены" : "Выключены",
                },
                {
                    label: "Подозрительная активность",
                    value: settings.suspicious_activity_notifications_enabled ? "Контролируется" : "Не контролируется",
                },
                {
                    label: "Доверенные устройства",
                    value: settings.trusted_devices_enabled ? "Включены" : "Выключены",
                },
                { label: "Сессии", value: getSessionLifetimeLabel(settings.session_lifetime_mode, locale) },
            ],
        }, locale),
        settings,
    };
}
