import type { SettingsSelectOptionModel } from "@/modules/settings/types/settings.types";

export const colorModeOptions: SettingsSelectOptionModel[] = [
    {
        value: "light",
        label: "Светлый",
    },
    {
        value: "dark",
        label: "Тёмный",
    },
    {
        value: "system",
        label: "Системный",
    },
];

export const densityOptions: SettingsSelectOptionModel[] = [
    {
        value: "compact",
        label: "Компактная",
    },
    {
        value: "comfortable",
        label: "Стандартная",
    },
    {
        value: "spacious",
        label: "Просторная",
    },
];

export const languageOptions: SettingsSelectOptionModel[] = [
    {
        value: "ru",
        label: "Русский",
    },
    {
        value: "en",
        label: "Английский",
    },
    {
        value: "de",
        label: "Немецкий",
    },
    {
        value: "fr",
        label: "Французский",
    },
];

export const notificationFrequencyOptions: SettingsSelectOptionModel[] = [
    {
        value: "instant",
        label: "Сразу",
        text: "Уведомление приходит сразу после события.",
    },
    {
        value: "daily",
        label: "Ежедневно",
        text: "События собираются в ежедневный дайджест.",
    },
    {
        value: "weekly",
        label: "Еженедельно",
        text: "События собираются в недельную сводку.",
    },
    {
        value: "disabled",
        label: "Отключено",
        text: "Уведомления по этой категории не приходят.",
    },
];

export const profileVisibilityOptions: SettingsSelectOptionModel[] = [
    {
        value: "public",
        label: "Публичный",
        text: "Профиль доступен максимально широко.",
    },
    {
        value: "organization",
        label: "Только организация",
        text: "Профиль виден участникам вашей образовательной организации.",
    },
    {
        value: "role_only",
        label: "Только связанные роли",
        text: "Профиль видят только пользователи с подходящими ролями.",
    },
    {
        value: "private",
        label: "Приватный",
        text: "Профиль максимально ограничен.",
    },
];

export const sessionLifetimeOptions: SettingsSelectOptionModel[] = [
    {
        value: "standard",
        label: "Стандартный",
        text: "Обычная длительность сессии для ежедневной работы.",
    },
    {
        value: "extended",
        label: "Расширенный",
        text: "Сессия живёт дольше на доверенных устройствах.",
    },
    {
        value: "strict",
        label: "Строгий",
        text: "Сессия завершается быстрее ради безопасности.",
    },
];
