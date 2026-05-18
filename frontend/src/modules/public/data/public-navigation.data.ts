import type {
    PublicFooterGroup,
    PublicNavigationItem,
    PublicSocialLink,
} from "@/modules/public/types/public.types";

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
