import type { RouteLocationRaw } from "vue-router";

export type DashboardRole =
    | "admin"
    | "teacher"
    | "student"
    | "parent";

export type DashboardTone =
    | "primary"
    | "success"
    | "warning"
    | "danger"
    | "violet"
    | "neutral";

export type DashboardCalendarEventType =
    | "lesson"
    | "checking"
    | "deadline"
    | "system"
    | "neutral";

export type DashboardCreateItemKind = "calendar" | "note";

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

export interface DashboardCreateItemModalCopy {
    title: string;
    description: string;
    titleLabel: string;
    textLabel: string;
    dateLabel: string;
    eventTypeLabel: string;
    submitLabel: string;
}

export interface DashboardCalendarEventThemeOption {
    value: DashboardCalendarEventType;
    label: string;
}

export interface DashboardCreateItemModalContent {
    closeOverlayLabel: string;
    closeButtonLabel: string;
    cancelLabel: string;
    calendar: DashboardCreateItemModalCopy;
    note: DashboardCreateItemModalCopy;
    calendarEventThemeOptions: DashboardCalendarEventThemeOption[];
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

export interface DashboardCalendarLegendItem {
    key: DashboardCalendarEventType;
    label: string;
}

export interface DashboardCalendarDayEvent {
    type: DashboardCalendarEventType;
}

export interface DashboardCalendarDay {
    date: string;
    day: number;
    dateLabel?: string;
    isToday?: boolean;
    isSelected?: boolean;
    isMuted?: boolean;
    isWeekend?: boolean;
    title: string;
    text: string;
    events?: DashboardCalendarDayEvent[];
}

export interface DashboardCalendarContent {
    title: string;
    monthLabel: string;
    previousMonthLabel: string;
    nextMonthLabel: string;
    weekdays: string[];
    legend?: DashboardCalendarLegendItem[];
    noteBadge?: string;
    createLabel?: string;
    fullCalendarLabel?: string;
    fullCalendarTo?: RouteLocationRaw;
}

export interface DashboardNotificationItem {
    id: string | number;
    title: string;
    text: string;
    icon: string;
    isNew?: boolean;
}

export interface DashboardNotificationsContent {
    title: string;
    items: DashboardNotificationItem[];
    createLabel?: string;
    emptyText?: string;
    actionLabel?: string;
    actionTo?: RouteLocationRaw;
}

export interface DashboardNoteItem {
    id: string | number;
    date: string;
    title: string;
    text: string;
}

export interface DashboardNotesContent {
    title: string;
    items: DashboardNoteItem[];
    createLabel?: string;
    emptyText?: string;
    actionLabel?: string;
    actionTo?: RouteLocationRaw;
}

export interface DashboardProfileAction {
    label: string;
    icon: string;
    to?: RouteLocationRaw;
    action?: "logout";
}

export interface DashboardProfilePanelContent {
    user: DashboardTopbarUser;
    title: string;
    subtitle: string;
    actions: DashboardProfileAction[];
}

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

export interface DashboardPageScaffoldModel {
    shell: DashboardShellConfig;
    calendarContent: DashboardCalendarContent;
    calendarDays: DashboardCalendarDay[];
    notifications: DashboardNotificationsContent;
    notes: DashboardNotesContent;
    profilePanel: DashboardProfilePanelContent;
    createModal?: DashboardCreateItemModalContent;
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
