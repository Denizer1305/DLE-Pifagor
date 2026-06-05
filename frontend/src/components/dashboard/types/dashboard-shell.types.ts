import type { RouteLocationRaw } from "vue-router";
import type { DashboardRole } from "@/components/dashboard/types/dashboard-common.types";

export interface DashboardBrand {
    logo: string;
    title: string;
    subtitle: string;
}

export interface DashboardUserProfile {
    fullName: string;
    roleLabel: string;
    avatarUrl?: string;
    avatarAlt: string;
}

export interface DashboardNavigationItem {
    key: string;
    label: string;
    description: string;
    icon: string;
    to: RouteLocationRaw;
    badge?: string | number;
    exact?: boolean;
}

export interface DashboardSidebarExtraAction {
    label: string;
    icon: string;
    to?: RouteLocationRaw;
    href?: string;
}

export interface DashboardSidebarExtraCard {
    variant: "ai" | "student" | "custom";
    title: string;
    subtitle: string;
    text: string;
    icon?: string;
    image?: {
        src: string;
        alt: string;
    };
    action: DashboardSidebarExtraAction;
}

export interface DashboardSearchConfig {
    placeholder: string;
    ariaLabel: string;
}

export interface DashboardTopbarLabels {
    menu: string;
    calendar: string;
    notifications: string;
    notes: string;
    profile: string;
    closePanel: string;
}

export interface DashboardTopbarUser {
    fullName: string;
    roleLabel: string;
    avatarUrl?: string;
    avatarAlt: string;
}

export interface DashboardFloatingPanelConfig {
    key: string;
    title: string;
    subtitle?: string;
    icon: string;
    ariaLabel: string;
    badge?: string | number;
}

export interface DashboardShellConfig {
    pageClass: string;
    role: DashboardRole;
    brand: DashboardBrand;
    profile: DashboardUserProfile;
    navigation: DashboardNavigationItem[];
    sidebarExtra?: DashboardSidebarExtraCard;
    search: DashboardSearchConfig;
    topbarLabels: DashboardTopbarLabels;
    topbarUser: DashboardTopbarUser;
}
