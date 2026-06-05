import type { RouteLocationRaw } from "vue-router";

export type PublicButtonVariant = "primary" | "secondary" | "light";

export interface PublicAction {
    label: string;
    to: RouteLocationRaw;
    variant?: PublicButtonVariant;
    icon?: string;
}

export interface AboutHeroContent {
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

export interface AboutSectionHeadContent {
    label: string;
    title: string;
    description: string;
}

export interface AboutStoryPoint {
    icon: string;
    title: string;
    text: string;
}

export interface AboutStorySideCard {
    icon: string;
    title: string;
    text: string;
}

export interface AboutStoryContent extends AboutSectionHeadContent {
    main: {
        title: string;
        paragraphs: string[];
        points: AboutStoryPoint[];
    };
    sideCards: AboutStorySideCard[];
    origin: {
        badgeIcon: string;
        badgeText: string;
        title: string;
        text: string;
        highlightIcon: string;
        highlightText: string;
        image: {
            src: string;
            alt: string;
        };
        overlayTitle: string;
        overlayText: string;
    };
}

export interface AboutMissionValue {
    title: string;
    text: string;
}

export interface AboutMissionSideCard {
    icon: string;
    title: string;
    text: string;
}

export interface AboutMissionContent extends AboutSectionHeadContent {
    lead: {
        kicker: string;
        title: string;
        paragraphs: string[];
    };
    values: AboutMissionValue[];
    sideCards: AboutMissionSideCard[];
}

export interface AboutRoadmapStepContent {
    title: string;
    text: string;
    points: string[];
}

export interface AboutRoadmapContent extends AboutSectionHeadContent {
    intro: string;
    steps: AboutRoadmapStepContent[];
}

export interface AboutTeamMember {
    name: string;
    role: string;
    text: string;
    image: {
        src: string;
        alt: string;
    };
}

export interface AboutTeamContent extends AboutSectionHeadContent {
    intro: {
        kicker: string;
        title: string;
        text: string;
        stats: {
            value: string;
            text: string;
        }[];
    };
    members: AboutTeamMember[];
}

export interface AboutGratitudeCardContent {
    icon: string;
    title: string;
    tag?: string;
    text: string;
    points?: string[];
}

export interface AboutGratitudeContent extends AboutSectionHeadContent {
    subtitle: string;
    leftCards: AboutGratitudeCardContent[];
    center: {
        icon: string;
        title: string;
        text: string;
        note: string;
    };
    rightCards: AboutGratitudeCardContent[];
}

export interface AboutCtaContent {
    title: string;
    text: string;
    note: string;
    actions: PublicAction[];
}

export interface AboutPageContent {
    hero: AboutHeroContent;
    story: AboutStoryContent;
    mission: AboutMissionContent;
    roadmap: AboutRoadmapContent;
    team: AboutTeamContent;
    gratitude: AboutGratitudeContent;
    cta: AboutCtaContent;
}
