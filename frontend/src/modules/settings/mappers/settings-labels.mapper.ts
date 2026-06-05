import { translateSettingsText } from "@/modules/settings/data/settings-translations.data";
import type { LocaleCode } from "@/stores/locale.store";

export function getThemeLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        light: "Классическая тема",
        blue: "Синяя тема",
        "light-blue": "Голубая тема",
        green: "Зелёная тема",
        orange: "Оранжевая тема",
        pinki: "Розовая тема",
        violet: "Фиолетовая тема",
        red: "Красная тема",
        yellow: "Жёлтая тема",
        dark: "Тёмная тема",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getColorModeLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        light: "Светлый",
        dark: "Тёмный",
        system: "Системный",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getDensityLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        compact: "Компактная",
        comfortable: "Стандартная",
        spacious: "Просторная",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getLanguageLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        ru: "Русский",
        en: "Английский",
        de: "Немецкий",
        fr: "Французский",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getFrequencyLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        instant: "Сразу",
        daily: "Ежедневно",
        weekly: "Еженедельно",
        disabled: "Выключено",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getProfileVisibilityLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        public: "Публичный",
        organization: "Организация",
        role_only: "Только роль",
        private: "Приватный",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getRoleLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        teacher: "Преподаватель",
        learner: "Студент",
        guardian: "Родитель",
        admin: "Администратор",
    };

    return translateSettingsText(labels[value] || value, locale);
}

export function getSessionLifetimeLabel(value: string, locale: LocaleCode = "ru"): string {
    const labels: Record<string, string> = {
        standard: "Стандартный режим",
        extended: "Расширенный режим",
        strict: "Строгий режим",
    };

    return translateSettingsText(labels[value] || value, locale);
}
