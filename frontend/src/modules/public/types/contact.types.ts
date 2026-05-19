import type { RouteLocationRaw } from "vue-router";

export type PublicContactActionVariant = "primary" | "secondary" | "light";

export type ContactFeedbackTopic =
    | "question"
    | "partnership"
    | "organization_connection"
    | "technical_support"
    | "bug"
    | "other";

export interface ContactFeedbackFormState {
    topic: ContactFeedbackTopic;
    fullName: string;
    email: string;
    phone: string;
    organizationName: string;
    subject: string;
    message: string;
    isPersonalDataConsent: boolean;
    attachments: File[];
}

export interface ContactFeedbackFormErrors {
    topic: string;
    fullName: string;
    email: string;
    phone: string;
    organizationName: string;
    subject: string;
    message: string;
    isPersonalDataConsent: string;
    attachments: string;
    common: string;
}

export interface ContactFeedbackPayload {
    topic: ContactFeedbackTopic;
    fullName: string;
    email: string;
    phone?: string;
    organizationName?: string;
    subject?: string;
    message: string;
    isPersonalDataConsent: boolean;
    pageUrl?: string;
    frontendRoute?: string;
    attachments?: File[];
}

export interface ContactFeedbackResponse {
    id: number;
    status: string;
    message: string;
}

export interface ContactFeedbackFieldContent {
    label: string;
    placeholder?: string;
    hint?: string;
}

export interface ContactFeedbackContent {
    label: string;
    title: string;
    description: string;
    topics: {
        value: ContactFeedbackTopic;
        label: string;
    }[];
    fields: {
        topic: ContactFeedbackFieldContent;
        name: ContactFeedbackFieldContent;
        email: ContactFeedbackFieldContent;
        phone: ContactFeedbackFieldContent;
        organization: ContactFeedbackFieldContent;
        subject: ContactFeedbackFieldContent;
        message: ContactFeedbackFieldContent;
        files: ContactFeedbackFieldContent;
        consent: string;
    };
    submitLabel: string;
    submittingLabel: string;
    successTitle: string;
    successText: string;
    resetLabel: string;
}

export interface PublicContactAction {
    label: string;
    to?: RouteLocationRaw;
    href?: string;
    icon?: string;
    variant?: PublicContactActionVariant;
}

export interface ContactHeroContent {
    badges: {
        icon: string;
        text: string;
    }[];
    title: string;
    subtitle: string;
    description: string;
    highlights: string[];
    actions: PublicContactAction[];
    logo: {
        src: string;
        alt: string;
    };
}

export interface ContactInfoItem {
    icon: string;
    title: string;
    text: string;
    href?: string;
}

export interface ContactActionChip {
    icon: string;
    label: string;
    href: string;
}

export interface ContactInfoCardContent {
    toplineIcon: string;
    topline: string;
    title: string;
    text: string;
    items: ContactInfoItem[];
    actions: ContactActionChip[];
}

export interface ContactHoursItem {
    title: string;
    text: string;
}

export interface ContactHoursCardContent {
    toplineIcon: string;
    topline: string;
    title: string;
    text: string;
    items: ContactHoursItem[];
}

export interface ContactSocialItem {
    icon?: string;
    image?: string;
    title: string;
    text: string;
    href: string;
}

export interface ContactSocialCardContent {
    toplineIcon: string;
    topline: string;
    title: string;
    text: string;
    items: ContactSocialItem[];
}

export interface ContactMapContent {
    toplineIcon: string;
    topline: string;
    title: string;
    text: string;
    address: string;
    mapTitle: string;
    mapSrc: string;
    fallbackText: string;
}

export interface ContactFindStep {
    number: string;
    title: string;
    text: string;
}

export interface ContactFindContent {
    toplineIcon: string;
    topline: string;
    title: string;
    text: string;
    steps: ContactFindStep[];
    notes: string[];
}

export interface ContactMainContent {
    label: string;
    title: string;
    description: string;
    info: ContactInfoCardContent;
    hours: ContactHoursCardContent;
    socials: ContactSocialCardContent;
    map: ContactMapContent;
    find: ContactFindContent;
}

export interface ContactCtaContent {
    title: string;
    text: string;
    note: string;
    actions: PublicContactAction[];
}

export interface ContactsPageContent {
    hero: ContactHeroContent;
    main: ContactMainContent;
    feedback: ContactFeedbackContent;
    cta: ContactCtaContent;
}