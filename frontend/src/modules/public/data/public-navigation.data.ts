import type {
    PublicFooterGroup,
    PublicNavigationItem,
    PublicSocialLink,
} from "@/modules/public/types/public.types";

export const publicNavigationItems: PublicNavigationItem[] = [
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
];

export const publicFooterGroups: PublicFooterGroup[] = [
    {
        title: "Платформа",
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
        title: "Пользователям",
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