export interface PublicNavigationItem {
    label: string;
    routeName: string;
    href?: string;
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