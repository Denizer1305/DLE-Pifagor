import type {
    DashboardAiCardContent,
    DashboardDayCardContent,
    DashboardHeroContent,
    DashboardHeroSectionContent,
    DashboardMiniPlanItem,
} from "@/components/dashboard/types/dashboard.types";

export type AdminDashboardHeroAction = DashboardHeroContent["actions"][number];

export type AdminDashboardHeroModel = DashboardHeroContent;

export type AdminDashboardDayStatModel = DashboardDayCardContent["stats"][number];

export type AdminDashboardDayCardModel = DashboardDayCardContent;

export type AdminDashboardTimelineItemModel = DashboardMiniPlanItem;

export interface AdminDashboardFeaturedStatModel {
    icon: string;
    title: string;
    value: number;
    label: string;
    progress: number;
}

export interface AdminDashboardCompactStatModel {
    key: string;
    icon: string;
    title: string;
    value: string | number;
    text: string;
}

export interface AdminDashboardAttentionItemModel {
    icon: string;
    title: string;
    text: string;
}

export interface AdminDashboardParticipantCardModel {
    icon: string;
    title: string;
    status: string;
    text: string;
    firstValue: string | number;
    firstLabel: string;
    secondValue: string | number;
    secondLabel: string;
    progressLabel: string;
    progress: number;
    actions: string[];
}

export interface AdminDashboardOverviewRowModel {
    section: string;
    state: string;
    value: string;
    status: string;
    warning: boolean;
}

export interface AdminDashboardEventModel {
    icon: string;
    title: string;
    text: string;
}

export interface AdminDashboardPageModel {
    hero: AdminDashboardHeroModel;
    dayCard: AdminDashboardDayCardModel;
    miniPlan: AdminDashboardTimelineItemModel[];
    heroSection: DashboardHeroSectionContent;

    featuredStat: AdminDashboardFeaturedStatModel;
    compactStats: AdminDashboardCompactStatModel[];

    planItems: AdminDashboardTimelineItemModel[];
    criticalItems: AdminDashboardAttentionItemModel[];
    participants: AdminDashboardParticipantCardModel[];
    recentEvents: AdminDashboardEventModel[];
    overviewRows: AdminDashboardOverviewRowModel[];
    ai: DashboardAiCardContent;
}
