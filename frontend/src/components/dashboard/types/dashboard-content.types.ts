import type { RouteLocationRaw } from "vue-router";
import type { DashboardTone } from "@/components/dashboard/types/dashboard-common.types";

export interface DashboardAction {
    label: string;
    icon?: string;
    description?: string;
    to?: RouteLocationRaw;
    href?: string;
    variant?: "primary" | "secondary";
}

export interface DashboardIntroBadge {
    label: string;
    icon: string;
}

export interface DashboardIntroContent {
    badges: DashboardIntroBadge[];
    title: string;
    text: string;
    actions: DashboardAction[];
}

export interface DashboardDayStat {
    value: string | number;
    label: string;
}

export interface DashboardDayCardContent {
    badge: string;
    icon: string;
    title: string;
    text: string;
    stats: DashboardDayStat[];
}

export interface DashboardMetricItem {
    label: string;
    value: string | number;
}

export interface DashboardStatsCardContent {
    key: string;
    title: string;
    text?: string;
    icon: string;
    value: string | number;
    caption?: string;
    progress?: number;
    tone?: DashboardTone;
}

export interface DashboardListItem {
    id: string | number;
    icon: string;
    title: string;
    text: string;
    meta?: string;
    tone?: DashboardTone;
}

export interface DashboardCardSectionContent {
    badge?: string;
    icon?: string;
    title: string;
    text?: string;
    action?: DashboardAction;
    items: DashboardListItem[];
    emptyText?: string;
}

export interface DashboardTimelineItem {
    id: string | number;
    time: string;
    title: string;
    text: string;
    tone?: DashboardTone;
}

export interface DashboardTimelineContent {
    badge?: string;
    icon?: string;
    title: string;
    text?: string;
    action?: DashboardAction;
    items: DashboardTimelineItem[];
    emptyText?: string;
}

export interface DashboardAiCardContent {
    image: {
        src: string;
        alt: string;
    };
    title: string;
    subtitle: string;
    text: string;
    action: DashboardAction;
    actions?: DashboardAction[];
}

export interface DashboardCourseMetaItem {
    value: string | number;
    label: string;
}

export interface DashboardCourseCardContent {
    id: string | number;
    icon: string;
    status: string;
    statusVariant?: "active" | "draft" | "warning";
    title: string;
    description: string;
    meta: DashboardCourseMetaItem[];
    progress?: number;
    progressLabel?: string;
    actions?: DashboardAction[];
}

export interface DashboardHeroAction {
    label: string;
    icon: string;
    routeName: string;
    variant?: "primary" | "secondary" | "light";
}

export interface DashboardHeroBadge {
    label: string;
    icon: string;
}

export interface DashboardHeroContent {
    badges: DashboardHeroBadge[];
    title: string;
    text: string;
    actions: DashboardHeroAction[];
}

export interface DashboardMiniPlanItem {
    time: string;
    title: string;
    text: string;
}

export interface DashboardHeroSectionContent {
    hero: DashboardHeroContent;
    dayCard: DashboardDayCardContent;
    miniPlan?: DashboardMiniPlanItem[];
    miniPlanTitle?: string;
    miniPlanIcon?: string;
}
