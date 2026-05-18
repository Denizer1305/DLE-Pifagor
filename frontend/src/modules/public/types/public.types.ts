export interface PublicNavigationItem {
    label: string;
    routeName: string;
    icon?: string;
    description?: string;
}

export interface PublicFooterLink {
    label: string;
    routeName: string;
}

export interface PublicFooterGroup {
    title: string;
    links: PublicFooterLink[];
}

export interface PublicSocialLink {
    label: string;
    href: string;
    icon: string;
}

export interface PublicBadgeItem {
    icon: string;
    label: string;
}

export interface PublicStatItem {
    value: string;
    label: string;
    description?: string;
}

export interface PublicFeatureItem {
    icon: string;
    title: string;
    description: string;
    points?: string[];
    accent?: string;
}

export interface PublicPartnerItem {
    name: string;
    description: string;
    icon: string;
    tag?: string;
}

export interface PublicTestimonialItem {
    name: string;
    role: string;
    text: string;
    icon: string;
    tone?: "left" | "featured" | "right";
}

export interface PublicCtaAction {
    label: string;
    routeName: string;
    variant: "primary" | "secondary";
}
