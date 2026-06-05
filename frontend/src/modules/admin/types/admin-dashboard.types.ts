import type {
    DashboardAiCardContent,
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardCardSectionContent,
    DashboardDayCardContent,
    DashboardIntroContent,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardProfilePanelContent,
    DashboardShellConfig,
    DashboardStatsCardContent,
    DashboardTimelineContent,
    DashboardTone,
} from "@/components/dashboard/types/dashboard.types";

export type AdminDashboardTone = DashboardTone;

export type AdminSystemStatus =
    | "ok"
    | "warning"
    | "critical";

export interface AdminDashboardProfileDto {
    id: number;
    full_name: string;
    email: string;
    avatar_url: string;
    role_label: string;
}

export interface AdminDashboardStatDto {
    key: string;
    label: string;
    value: number;
    caption: string;
    icon: string;
    tone: AdminDashboardTone;
}

export interface AdminDashboardCalendarDayDto {
    date: string;
    day: number;
    is_today: boolean;
    is_selected: boolean;
    is_muted: boolean;
    is_weekend: boolean;
    title: string;
    text: string;
}

export interface AdminDashboardCalendarDto {
    month_label: string;
    selected_date: string;
    days: AdminDashboardCalendarDayDto[];
}

export interface AdminDashboardUserShortDto {
    id: number;
    full_name: string;
    email: string;
    status: string;
    created_at: string;
}

export interface AdminDashboardOrganizationShortDto {
    id: number;
    name: string;
}

export interface AdminDashboardDepartmentShortDto {
    id: number;
    name: string;
}

export interface AdminDashboardGroupShortDto {
    id: number;
    name: string;
}

export interface AdminDashboardJoinRequestDto {
    id: number;
    request_type: string;
    status: string;
    user: AdminDashboardUserShortDto;
    organization: AdminDashboardOrganizationShortDto | null;
    department: AdminDashboardDepartmentShortDto | null;
    group: AdminDashboardGroupShortDto | null;
    message: string;
    created_at: string;
}

export interface AdminDashboardFeedbackRequestDto {
    id: number;
    full_name: string;
    email: string;
    topic: string;
    status: string;
    message: string;
    created_at: string;
}

export interface AdminDashboardAuditActorDto {
    id: number;
    full_name: string;
    email: string;
}

export interface AdminDashboardAuditEventDto {
    id: number;
    action: string;
    message: string;
    actor: AdminDashboardAuditActorDto | null;
    target_user: AdminDashboardAuditActorDto | null;
    created_at: string;
}

export interface AdminDashboardSystemCheckDto {
    key: string;
    label: string;
    status: AdminSystemStatus;
    text: string;
    icon: string;
}

export interface AdminDashboardSystemHealthDto {
    status: AdminSystemStatus;
    checks: AdminDashboardSystemCheckDto[];
}

export interface AdminDashboardQuickActionDto {
    key: string;
    label: string;
    description: string;
    icon: string;
    route_name: string;
    tone: AdminDashboardTone;
}

export interface AdminDashboardSummaryDto {
    profile: AdminDashboardProfileDto;
    stats: AdminDashboardStatDto[];
    calendar: AdminDashboardCalendarDto;
    recent_users: AdminDashboardUserShortDto[];
    join_requests: AdminDashboardJoinRequestDto[];
    feedback_requests: AdminDashboardFeedbackRequestDto[];
    audit_events: AdminDashboardAuditEventDto[];
    system_health: AdminDashboardSystemHealthDto;
    quick_actions: AdminDashboardQuickActionDto[];
}

export interface AdminDashboardProfile {
    id: number;
    fullName: string;
    email: string;
    avatarUrl: string;
    roleLabel: string;
}

export interface AdminDashboardStat {
    key: string;
    label: string;
    value: number;
    caption: string;
    icon: string;
    tone: AdminDashboardTone;
}

export interface AdminDashboardCalendar {
    monthLabel: string;
    selectedDate: string;
    days: DashboardCalendarDay[];
}

export interface AdminDashboardUserShort {
    id: number;
    fullName: string;
    email: string;
    status: string;
    createdAt: string;
}

export interface AdminDashboardJoinRequest {
    id: number;
    requestType: string;
    status: string;
    user: AdminDashboardUserShort;
    organization: AdminDashboardOrganizationShortDto | null;
    department: AdminDashboardDepartmentShortDto | null;
    group: AdminDashboardGroupShortDto | null;
    message: string;
    createdAt: string;
}

export interface AdminDashboardFeedbackRequest {
    id: number;
    fullName: string;
    email: string;
    topic: string;
    status: string;
    message: string;
    createdAt: string;
}

export interface AdminDashboardAuditActor {
    id: number;
    fullName: string;
    email: string;
}

export interface AdminDashboardAuditEvent {
    id: number;
    action: string;
    message: string;
    actor: AdminDashboardAuditActor | null;
    targetUser: AdminDashboardAuditActor | null;
    createdAt: string;
}

export interface AdminDashboardSystemCheck {
    key: string;
    label: string;
    status: AdminSystemStatus;
    text: string;
    icon: string;
}

export interface AdminDashboardSystemHealth {
    status: AdminSystemStatus;
    checks: AdminDashboardSystemCheck[];
}

export interface AdminDashboardQuickAction {
    key: string;
    label: string;
    description: string;
    icon: string;
    routeName: string;
    tone: AdminDashboardTone;
}

export interface AdminDashboardSummary {
    profile: AdminDashboardProfile;
    stats: AdminDashboardStat[];
    calendar: AdminDashboardCalendar;
    recentUsers: AdminDashboardUserShort[];
    joinRequests: AdminDashboardJoinRequest[];
    feedbackRequests: AdminDashboardFeedbackRequest[];
    auditEvents: AdminDashboardAuditEvent[];
    systemHealth: AdminDashboardSystemHealth;
    quickActions: AdminDashboardQuickAction[];
}

export interface AdminDashboardViewModel {
    shell: DashboardShellConfig;
    calendarContent: DashboardCalendarContent;
    calendarDays: DashboardCalendarDay[];
    notifications: DashboardNotificationsContent;
    notes: DashboardNotesContent;
    profilePanel: DashboardProfilePanelContent;
    intro: DashboardIntroContent;
    dayCard: DashboardDayCardContent;
    stats: DashboardStatsCardContent[];
    quickActions: AdminDashboardQuickAction[];
    recentUsers: DashboardCardSectionContent;
    joinRequests: DashboardCardSectionContent;
    feedbackRequests: DashboardCardSectionContent;
    audit: DashboardTimelineContent;
    systemHealth: DashboardCardSectionContent;
    ai: DashboardAiCardContent;
}
