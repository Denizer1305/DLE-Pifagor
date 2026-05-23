import type { RouteLocationRaw } from "vue-router";

import heroLogo from "@/assets/brand/logo/themes/light/hero-logo.svg";
import anastasiaLogo from "@/assets/brand/logo/themes/light/Anastasia.svg";

import elros from "@/assets/image/avatars/elros.webp";
import vamk from "@/assets/image/avatars/vamk.webp";

import fotoTeachers from "@/assets/image/avatars/foto_teachers.webp";
import denizer1305 from "@/assets/image/avatars/denizer1305.webp";
import anastasiaQe from "@/assets/image/avatars/anastasia_qe.webp";

export type PublicButtonVariant = "primary" | "secondary" | "light";

export interface PublicAction {
    label: string;
    to: RouteLocationRaw;
    variant?: PublicButtonVariant;
    icon?: string;
}

export interface HomeHeroContent {
    badges: {
        icon: string;
        text: string;
    }[];
    title: string;
    subtitle: string;
    description: string;
    highlights: string[];
    actions: PublicAction[];
    logo: {
        src: string;
        alt: string;
    };
}

export interface HomeFeatureCardData {
    label: string;
    icon: string;
    title: string;
    description: string;
    variant?: string;
    points?: string[];
    icons?: string[];
    chips?: {
        title: string;
        text: string;
    }[];
    stats?: {
        value: string;
        text: string;
    }[];
    hasDiagram?: boolean;
    hasOrbit?: boolean;
}

export interface HomeFeaturesContent {
    label: string;
    title: string;
    description: string;
    mainCards: HomeFeatureCardData[];
    sideCards: HomeFeatureCardData[];
}

export interface HomeAiCardData {
    variant?: string;
    label: string;
    icon: string;
    title: string;
    text: string;
    points?: string[];
    logic?: {
        title: string;
        text: string;
    }[];
    quote?: string;
    quoteSub?: string;
}

export interface HomeAiMiniCardData {
    icon: string;
    title: string;
    text: string;
}

export interface HomeAiContent {
    label: string;
    title: string;
    description: string;
    avatar: {
        src: string;
        alt: string;
    };
    cards: HomeAiCardData[];
    miniCards: HomeAiMiniCardData[];
}

export interface HomePartnerItem {
    variant?: string;
    tag: string;
    name: string;
    text: string;
    image: {
        src: string;
        alt: string;
    };
}

export interface HomePartnersContent {
    label: string;
    title: string;
    description: string;
    intro: {
        label: string;
        title: string;
        text: string;
    };
    accent: {
        icon: string;
        title: string;
        text: string;
    };
    items: HomePartnerItem[];
}

export interface HomeTestimonialItem {
    variant?: string;
    name: string;
    text: string;
    image: {
        src: string;
        alt: string;
    };
}

export interface HomeTestimonialsContent {
    label: string;
    title: string;
    description: string;
    items: HomeTestimonialItem[];
}

export interface HomeCtaContent {
    title: string;
    text: string;
    actions: PublicAction[];
}

export interface HomePageContent {
    hero: HomeHeroContent;
    features: HomeFeaturesContent;
    ai: HomeAiContent;
    partners: HomePartnersContent;
    testimonials: HomeTestimonialsContent;
    cta: HomeCtaContent;
}

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

export const homeFeatures: HomeFeaturesContent = {
    label: "Возможности платформы",
    title: "Система, где каждый блок работает на обучение",
    description:
        "«Пифагор» объединяет ключевые процессы образовательной среды в одном пространстве: от создания материалов до контроля успеваемости, аналитики и взаимодействия между участниками.",
    mainCards: [
        {
            variant: "hero-card",
            icon: "fas fa-grid-2",
            label: "Единая цифровая среда",
            title: "Все ключевые процессы собраны в одной платформе",
            description:
                "Курсы, тесты, практические и домашние задания, электронный журнал, расписание, аналитика и взаимодействие между преподавателем, студентом и родителем работают как единая экосистема без разрозненных сервисов.",
            points: [
                "Единая точка входа для всех ролей.",
                "Централизованное управление учебным процессом.",
                "Последовательная логика интерфейсов и сценариев.",
                "Быстрое масштабирование от одного курса до целой образовательной организации.",
            ],
            hasOrbit: true,
        },
        {
            variant: "wide-card",
            icon: "fas fa-book-open",
            label: "Курсы и материалы",
            title: "Конструктор учебного контента",
            description:
                "Платформа помогает выстраивать модули, уроки, задания и материалы в логичную структуру, удобную как для преподавателя, так и для обучающегося.",
            points: [
                "Модули, уроки и темы в единой архитектуре курса.",
                "Поддержка текста, видео, практики и сопроводительных материалов.",
                "Простой переход от методической идеи к готовому цифровому курсу.",
            ],
            icons: [
                "fas fa-folder-tree",
                "fas fa-file-lines",
                "fas fa-video",
                "fas fa-pen-ruler",
            ],
        },
        {
            variant: "tall-card",
            icon: "fas fa-chart-line",
            label: "Аналитика и контроль",
            title: "Прогресс, посещаемость и результаты в динамике",
            description:
                "Система собирает показатели успеваемости и делает их понятными: видно сильные стороны, проблемные темы и общую картину по группам.",
            hasDiagram: true,
            stats: [
                {
                    value: "24/7",
                    text: "доступ к данным и учебной статистике",
                },
                {
                    value: "360°",
                    text: "обзор учебного процесса по ролям",
                },
            ],
        },
    ],
    sideCards: [
        {
            variant: "stack-card",
            icon: "fas fa-list-check",
            label: "Оценивание",
            title: "Проверка знаний и заданий",
            description:
                "Поддержка тестирования, практических работ и домашней деятельности с удобной логикой проверки, оценивания и обратной связи.",
            chips: [
                {
                    title: "Тесты",
                    text: "мгновенная проверка",
                },
                {
                    title: "Практика",
                    text: "гибкие сценарии",
                },
                {
                    title: "Домашние",
                    text: "пошаговый контроль",
                },
                {
                    title: "Комментарии",
                    text: "обратная связь",
                },
            ],
            points: [
                "Поддержка прозрачных критериев оценки.",
                "Фиксация результатов и история проверки в одном месте.",
            ],
        },
        {
            variant: "small-card",
            icon: "fas fa-calendar-days",
            label: "Журнал и расписание",
            title: "Организация учебного ритма",
            description:
                "Оценки, посещаемость, расписание и статусы учебной активности в едином контуре.",
            points: [
                "Удобная навигация по занятиям, датам и событиям.",
                "Понятная картина учебной недели для всех участников.",
            ],
        },
        {
            variant: "small-card-2",
            icon: "fas fa-users",
            label: "Связь участников",
            title: "Преподаватель, студент и родитель в одном поле",
            description:
                "Прозрачное взаимодействие между всеми участниками образовательного процесса.",
            points: [
                "Родители видят реальную картину прогресса и посещаемости.",
                "Преподаватель быстрее реагирует на изменения в обучении.",
            ],
        },
    ],
};

export const homeAi: HomeAiContent = {
    label: "ИИ-Анастасия",
    title: "Именная нейросеть, которая становится цифровым союзником преподавателя",
    description:
        "Анастасия — это интеллектуальный помощник внутри платформы. Она помогает преподавателю работать с учебным процессом, а студенту — спокойнее ориентироваться в обучении.",
    avatar: {
        src: anastasiaLogo,
        alt: "ИИ-Анастасия",
    },
    cards: [
        {
            variant: "ai-hero-card",
            icon: "fas fa-wand-magic-sparkles",
            label: "Входит в работу",
            title: "Анастасия рядом в ежедневной работе преподавателя",
            text:
                "Она помогает быстрее ориентироваться в учебных материалах, заданиях, результатах и действиях внутри платформы.",
            points: [
                "подсказывает следующие действия",
                "помогает работать с учебными материалами",
                "объясняет сложные элементы простыми словами",
            ],
        },
        {
            variant: "ai-logic-card",
            icon: "fas fa-brain",
            label: "При опоре её работы",
            title: "Три опоры её работы",
            text:
                "Анастасия не заменяет преподавателя. Она дополняет образовательную среду и помогает сделать взаимодействие понятнее.",
            logic: [
                {
                    title: "Понять",
                    text: "объяснить тему",
                },
                {
                    title: "Найти",
                    text: "показать раздел",
                },
                {
                    title: "Подсказать",
                    text: "следующее действие",
                },
            ],
        },
        {
            variant: "ai-voice-card",
            icon: "fas fa-heart",
            label: "Характер общения",
            title: "У Анастасии есть собственный тон общения",
            text:
                "Она отвечает спокойно, доброжелательно и без давления, сохраняя стиль образовательной платформы.",
            quote:
                "«Здравствуйте! Я Анастасия. Давайте разберёмся спокойно и по шагам. Мы с вами справимся.»",
            quoteSub:
                "Такой тон делает цифровую среду человечнее и понятнее.",
        },
    ],
    miniCards: [
        {
            icon: "fas fa-comments",
            title: "Нежная поддержка",
            text: "подсказывает без давления",
        },
        {
            icon: "fas fa-route",
            title: "Навигация по платформе",
            text: "помогает найти нужный раздел",
        },
        {
            icon: "fas fa-lightbulb",
            title: "Объяснение",
            text: "сложное простыми словами",
        },
    ],
};

export const homePartners: HomePartnersContent = {
    label: "Партнёры",
    title: "Платформа развивается вместе с сильными и реальными партнерами",
    description:
        "Здесь мы показываем тех, кто помогает платформе быть устойчивой, современной и полезной в реальной работе.",
    intro: {
        label: "Партнёрская экосистема",
        title:
            "Партнёры, которые помогают платформе быть устойчивой, современной и полезной в реальной работе",
        text:
            "Мы рассматриваем Пифагор как открытую образовательную экосистему, которая может развиваться вместе с образовательными организациями и технологическими партнёрами.",
    },
    accent: {
        icon: "fas fa-network-wired",
        title: "Партнёрство в действии",
        text:
            "Сильная цифровая среда появляется там, где образование, технологии и реальные пользователи работают вместе.",
    },
    items: [
        {
            variant: "left",
            tag: "Технологический партнёр",
            name: "ООО «ЭЛРОС»",
            text:
                "Технологическое партнёрство и поддержка развития цифровой образовательной среды.",
            image: {
                src: elros,
                alt: "ООО «ЭЛРОС»",
            },
        },
        {
            variant: "right",
            tag: "Образовательный партнёр",
            name: "ГАПОУ ВО «ВлГК им. Советкина»",
            text:
                "Образовательная среда, на базе которой формируется практическое понимание задач платформы.",
            image: {
                src: vamk,
                alt: "ГАПОУ ВО «ВлГК им. Советкина»",
            },
        },
    ],
};

export const homeTestimonials: HomeTestimonialsContent = {
    label: "Отзывы",
    title: "Платформу уже оценивают реальные участники образовательного процесса",
    description:
        "Мы собираем обратную связь от тех, кто каждый день работает с обучением, заданиями, расписанием и результатами.",
    items: [
        {
            variant: "left",
            name: "Олег Новиков",
            text:
                "Как родитель, я ценю возможность в любой момент посмотреть успеваемость своего ребенка. Платформа даёт полную картину его прогресса и вовремя предупреждает о проблемах.",
            image: {
                src: denizer1305,
                alt: "Олег Новиков",
            },
        },
        {
            variant: "featured",
            name: "Татьяна Икрамова",
            text:
                "«Пифагор» кардинально изменила мой подход к преподаванию. Теперь я могу легко создавать интерактивные задания и отслеживать прогресс каждого студента в реальном времени.",
            image: {
                src: fotoTeachers,
                alt: "Татьяна Икрамова",
            },
        },
        {
            variant: "right",
            name: "Мария Фролова",
            text:
                "Благодаря «Пифагору» я наконец-то разобралась с высшей математикой. Интерактивные задания и мгновенная проверка помогают сразу понять свои ошибки и исправить их.",
            image: {
                src: anastasiaQe,
                alt: "Мария Фролова",
            },
        },
    ],
};

export const homeCta: HomeCtaContent = {
    title: "Пора переходить к новой цифровой среде образования",
    text:
        "Подключайтесь к среде «Пифагор», чтобы объединить обучение, контроль, аналитику и ИИ-помощника в одном пространстве. Это российская система, созданная для современного образовательного процесса и ежедневной работы преподавателей.",
    actions: [
        {
            label: "Попробовать",
            to: {
                name: "register",
            },
            variant: "primary",
            icon: "fas fa-arrow-right",
        },
        {
            label: "Подробнее",
            to: {
                name: "about",
            },
            variant: "secondary",
        },
    ],
};

export const homePageContent: HomePageContent = {
    hero: homeHero,
    features: homeFeatures,
    ai: homeAi,
    partners: homePartners,
    testimonials: homeTestimonials,
    cta: homeCta,
};
