import type { RouteLocationRaw } from "vue-router";

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
