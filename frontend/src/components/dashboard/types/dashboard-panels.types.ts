import type { RouteLocationRaw } from "vue-router";
import type { DashboardShellConfig, DashboardTopbarUser } from "@/components/dashboard/types/dashboard-shell.types";

export type DashboardCalendarEventType =
    | "lesson"
    | "checking"
    | "deadline"
    | "system"
    | "neutral";

export type DashboardCreateItemKind = "calendar" | "note";

export interface DashboardCreateItemModalCopy {
    title: string;
    description: string;
    titleLabel: string;
    textLabel: string;
    dateLabel: string;
    eventTypeLabel: string;
    notificationLabel: string;
    notificationText: string;
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
    savingLabel: string;
    calendar: DashboardCreateItemModalCopy;
    note: DashboardCreateItemModalCopy;
    calendarEventThemeOptions: DashboardCalendarEventThemeOption[];
}

export interface DashboardCalendarLegendItem {
    key: DashboardCalendarEventType;
    label: string;
}

export interface DashboardCalendarDayEvent {
    type: DashboardCalendarEventType;
}

export interface DashboardCalendarDay {
    itemId?: number;
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
    removeLabel?: string;
    fullCalendarLabel?: string;
    fullCalendarTo?: RouteLocationRaw;
}

export interface DashboardNotificationItem {
    id: string | number;
    title: string;
    text: string;
    icon: string;
    isNew?: boolean;
    actionLabel?: string;
    actionTo?: RouteLocationRaw;
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
    itemId?: number;
    date: string;
    title: string;
    text: string;
}

export interface DashboardNotesContent {
    title: string;
    items: DashboardNoteItem[];
    createLabel?: string;
    removeLabel?: string;
    readLabel?: string;
    closeLabel?: string;
    modalTitle?: string;
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

export interface DashboardPageScaffoldModel {
    shell: DashboardShellConfig;
    calendarContent: DashboardCalendarContent;
    calendarDays: DashboardCalendarDay[];
    notifications: DashboardNotificationsContent;
    notes: DashboardNotesContent;
    profilePanel: DashboardProfilePanelContent;
    createModal?: DashboardCreateItemModalContent;
}
