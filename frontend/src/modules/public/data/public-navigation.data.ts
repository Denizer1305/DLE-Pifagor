import type {
    PublicAccountMenuContent,
    PublicFooterGroup,
    PublicNavigationItem,
    PublicSocialLink,
} from "@/modules/public/types/public.types";
import { ROLE_CODES, ROLE_LABELS, type RoleCode } from "@/app/constants/roles.constants";
import { getDashboardRouteNameByRole } from "@/modules/auth/utils/auth-redirect.utils";

import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export const publicNavigationItems: PublicNavigationItem[] = [
    {
        label: "Главная",
        routeName: "home",
        icon: "fa-solid fa-house",
        description: "Приветственная страница платформы",
    },
    {
        label: "О платформе",
        routeName: "about",
        icon: "fa-solid fa-circle-info",
        description: "История, миссия и развитие",
    },
    {
        label: "Преподаватели",
        routeName: "teachers",
        icon: "fa-solid fa-chalkboard-user",
        description: "Педагоги образовательной организации",
    },
    {
        label: "Контакты",
        routeName: "contacts",
        icon: "fa-solid fa-envelope",
        description: "Связаться с командой проекта",
    },
];

export const publicFooterGroups: PublicFooterGroup[] = [
    {
        title: "Навигация",
        links: [
            {
                label: "Главная",
                routeName: "home",
            },
            {
                label: "О платформе",
                routeName: "about",
            },
            {
                label: "Преподаватели",
                routeName: "teachers",
            },
            {
                label: "Контакты",
                routeName: "contacts",
            },
        ],
    },
    {
        title: "Аккаунт",
        links: [
            {
                label: "Войти",
                routeName: "login",
            },
            {
                label: "Регистрация",
                routeName: "register",
            },
        ],
    },
];

export const publicSocialLinks: PublicSocialLink[] = [
    {
        label: "Email",
        href: "mailto:Pifagor-Platform33@yandex.ru",
        icon: "fa-solid fa-envelope",
    },
    {
        label: "Поддержка",
        href: "mailto:Pifagor-Platform33@yandex.ru",
        icon: "fa-solid fa-headset",
    },
];

interface PublicAccountMenuSource {
    fullName: string;
    email: string;
    avatarUrl: string;
    activeRole: RoleCode | "";
    isSuperuser: boolean;
}

export function createPublicAccountMenuContent(
    source: PublicAccountMenuSource,
): PublicAccountMenuContent {
    const roleCode = source.isSuperuser
        ? ROLE_CODES.SUPERADMIN
        : source.activeRole;
    const fullName = source.fullName || source.email || "Пользователь";

    return {
        openLabel: "Открыть меню профиля",
        closeLabel: "Закрыть меню профиля",
        user: {
            fullName,
            roleLabel: roleCode ? ROLE_LABELS[roleCode] : "Пользователь",
            avatarUrl: source.avatarUrl || fallbackAvatar,
            avatarAlt: `Профиль пользователя ${fullName}`,
        },
        title: "Личный кабинет",
        subtitle: "Управление профилем и настройками",
        actions: [
            {
                label: "Перейти в кабинет",
                icon: "fa-solid fa-table-columns",
                routeName: getDashboardRouteNameByRole(
                    source.activeRole,
                    source.isSuperuser,
                ),
            },
            {
                label: "Мой профиль",
                icon: "fa-solid fa-user",
                routeName: "profile",
            },
            {
                label: "Выйти",
                icon: "fa-solid fa-arrow-right-from-bracket",
                action: "logout",
            },
        ],
    };
}
