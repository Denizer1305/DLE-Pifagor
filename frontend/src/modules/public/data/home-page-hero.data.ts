import heroLogo from "@/assets/brand/logo/themes/light/hero-logo.svg";
import type { HomeHeroContent } from "@/modules/public/data/home-page.types";

export const homeHero: HomeHeroContent = {
    badges: [
        {
            icon: "fas fa-flag",
            text: "Российская платформа для российского образования",
        },
        {
            icon: "fas fa-shield-alt",
            text: "Отечественная разработка единой цифровой среды",
        },
    ],
    title: "Цифровая образовательная среда Пифагор",
    subtitle: "Отечественная образовательная платформа нового поколения",
    description:
        "«Пифагор» объединяет обучение, контроль знаний, курсы, тестирование, практические работы, журнал, расписание, аналитику и интеллектуальную помощь в одном пространстве.",
    highlights: [
        "Единая цифровая среда для обучения, управления и аналитики.",
        "Спокойный, понятный и лаконичный интерфейс без перегруза.",
        "Современный российский продукт для образовательных организаций.",
    ],
    actions: [
        {
            label: "Начать обучение",
            to: {
                name: "register",
            },
            variant: "primary",
            icon: "fas fa-arrow-right",
        },
        {
            label: "О платформе",
            to: {
                name: "about",
            },
            variant: "secondary",
        },
    ],
    logo: {
        src: heroLogo,
        alt: "ЦОС «Пифагор»",
    },
};
