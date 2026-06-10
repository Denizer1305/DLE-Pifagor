import type { SettingsCenterCardModel } from "@/modules/settings/types/settings.types";

export const settingsCenterCards: SettingsCenterCardModel[] = [
    {
        key: "security",
        icon: "fas fa-shield-halved",
        title: "Безопасность",
        text:
            "Пароль, активные сессии, уведомления о входах и дополнительные меры защиты аккаунта.",
        badge: "Важно",
        routeName: "settings-security",
    },
    {
        key: "notifications",
        icon: "fas fa-bell",
        title: "Уведомления",
        text:
            "Каналы доставки, частота уведомлений, учебные события, системные сообщения и дайджесты.",
        badge: "12 событий",
        routeName: "settings-notifications",
    },
    {
        key: "appearance",
        icon: "fas fa-palette",
        title: "Внешний вид",
        text:
            "Цветовая схема, светлый или тёмный режим, плотность интерфейса, анимации и карточки.",
        badge: "Сразу применяется",
        routeName: "settings-appearance",
    },
    {
        key: "privacy",
        icon: "fas fa-user-lock",
        title: "Приватность",
        text:
            "Видимость профиля, контактов, ролевых данных, достижений и доступ по ролям.",
        badge: "Персонально",
        routeName: "settings-privacy",
    },
    {
        key: "roles",
        icon: "fas fa-user-gear",
        title: "Ролевые настройки",
        text:
            "Настройка поведения личного кабинета под активную роль пользователя.",
        badge: "Гибко",
        routeName: "settings-roles",
    },
    {
        key: "profile",
        icon: "fas fa-id-badge",
        title: "Профиль",
        text:
            "Личные данные, аватар, контакты и ролевой профиль пользователя.",
        badge: "Аккаунт",
        routeName: "profile",
    },
];
