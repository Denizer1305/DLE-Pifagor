import heroLogo from "@/assets/brand/logo/themes/light/hero-logo.svg";
import type {
    ContactCtaContent,
    ContactHeroContent,
} from "@/modules/public/types/contact.types";

export const contactHeroContent: ContactHeroContent = {
    badges: [
        {
            icon: "fas fa-location-dot",
            text: "Адрес и карта",
        },
        {
            icon: "fas fa-comments",
            text: "Всегда на связи",
        },
    ],
    title: "Контакты",
    subtitle:
        "Если у вас есть вопрос, предложение или интерес к сотрудничеству — мы всегда открыты к диалогу",
    description:
        "Здесь вы найдёте адрес, электронную почту, телефон и карту с точкой расположения. Всё самое важное собрано в одном месте, чтобы связаться с нами было легко и удобно.",
    highlights: [
        "Быстро найти адрес и построить маршрут.",
        "Написать нам по почте или связаться по телефону.",
        "Обсудить использование платформы или возможное партнёрство.",
    ],
    actions: [
        {
            label: "Смотреть контакты",
            href: "#contact-main",
            variant: "primary",
            icon: "fas fa-arrow-right",
        },
        {
            label: "Открыть карту",
            href: "#contact-map",
            variant: "light",
        },
    ],
    logo: {
        src: heroLogo,
        alt: "ЦОС «Пифагор»",
    },
};

export const contactCtaContent: ContactCtaContent = {
    title: "Будем рады вашему сообщению",
    text:
        "Если вы хотите задать вопрос, обсудить внедрение платформы или предложить сотрудничество, напишите нам или свяжитесь по телефону. Мы открыты к общению, идеям и сильным партнёрствам.",
    note:
        "Мы ценим живой диалог, внимательную обратную связь и долгосрочное сотрудничество.",
    actions: [
        {
            label: "Написать нам",
            href: "mailto:Pifagor-Platform33@yandex.ru",
            variant: "primary",
            icon: "fas fa-arrow-right",
        },
        {
            label: "Позвонить",
            href: "tel:+79000000000",
            variant: "secondary",
        },
    ],
};
