import type {
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardCourseCardContent,
    DashboardDayCardContent,
    DashboardHeroContent,
    DashboardHeroSectionContent,
    DashboardListItem,
    DashboardMiniPlanItem,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardPageScaffoldModel,
    DashboardStatsCardContent,
    DashboardTimelineItem,
} from "@/components/dashboard/types/dashboard.types";

export interface ParentDashboardModel extends DashboardPageScaffoldModel {
    hero: DashboardHeroContent;
    dayCard: DashboardDayCardContent;
    miniPlan: DashboardMiniPlanItem[];
    heroSection: DashboardHeroSectionContent;

    stats: DashboardStatsCardContent[];

    scheduleSection: ParentDashboardSectionContent;
    schedule: DashboardTimelineItem[];

    notificationsSection: ParentDashboardSectionContent;
    importantItems: DashboardListItem[];

    coursesSection: ParentDashboardSectionContent;
    courses: DashboardCourseCardContent[];

    activitySection: ParentDashboardSectionContent;
    activityItems: DashboardListItem[];

    gradesSection: ParentDashboardSectionContent;
    gradeRows: ParentGradeRow[];

    messagesSection: ParentDashboardSectionContent;
    messages: DashboardListItem[];
}

export interface ParentDashboardSectionContent {
    badge: string;
    icon: string;
    title: string;
    text: string;
    emptyIcon: string;
    emptyText: string;
}

export interface ParentGradeRow {
    id: string | number;
    subject: string;
    work: string;
    grade: string;
    status: string;
    warning?: boolean;
}

export interface ParentDashboardProfile {
    id: number;
    fullName: string;
    email: string;
    avatarUrl: string;
    roleLabel: string;
}

export interface ParentDashboardSummary {
    profile: ParentDashboardProfile;
    calendar: {
        monthLabel: string;
        selectedDate: string;
        days: DashboardCalendarDay[];
    };
    stats: DashboardStatsCardContent[];
    dayStats: {
        lessons: number;
        assignments: number;
        messages: number;
    };
    schedule: DashboardTimelineItem[];
    courses: DashboardCourseCardContent[];
    importantItems: DashboardListItem[];
    activityItems: DashboardListItem[];
    gradeRows: ParentGradeRow[];
    messages: DashboardListItem[];
    notifications: DashboardNotificationsContent["items"];
    notes: DashboardNotesContent["items"];
}

export type ParentCalendarContent = DashboardCalendarContent;
