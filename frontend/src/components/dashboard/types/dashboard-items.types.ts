import type {
    DashboardCalendarEventType,
    DashboardCreateItemKind,
} from "@/components/dashboard/types/dashboard-panels.types";

export interface DashboardItemDto {
    id: number;
    kind: DashboardCreateItemKind;
    title: string;
    text: string;
    date: string;
    event_type: DashboardCalendarEventType;
    notification_enabled: boolean;
    created_at: string;
}

export interface DashboardItemCreatePayload {
    kind: DashboardCreateItemKind;
    title: string;
    text: string;
    date: string;
    eventType: DashboardCalendarEventType;
    notificationEnabled: boolean;
}
