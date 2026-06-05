import type {
    DashboardAiCardContent,
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardCreateItemModalContent,
    DashboardDayCardContent,
    DashboardHeroContent,
    DashboardHeroSectionContent,
    DashboardMiniPlanItem,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";
import type {
    TeacherDashboardActivityItem,
    TeacherDashboardAttentionItem,
} from "@/modules/teacher/types/teacher-dashboard-domain.types";

export type TeacherDashboardHeroActionModel = DashboardHeroContent["actions"][number];

export type TeacherDashboardHeroModel = DashboardHeroContent;

export interface TeacherDashboardFeaturedStatModel {
    icon: string;
    title: string;
    value: string | number;
    label: string;
    progress: number;
}

export interface TeacherDashboardCompactStatModel {
    key: string;
    icon: string;
    title: string;
    value: string | number;
    text: string;
}

export type TeacherDashboardTimelineItemModel = DashboardMiniPlanItem;

export interface TeacherDashboardCourseCardModel {
    id: number | string;
    icon: string;
    title: string;
    description: string;
    status: string;
    statusVariant: "active" | "draft" | "warning";
    modulesCount: number;
    studentsCount: number;
    progress: number;
}

export interface TeacherDashboardJournalRowModel {
    id: number | string;
    student: string;
    work: string;
    grade: string;
    status: string;
    warning: boolean;
}

export interface TeacherDashboardPageModel {
    hero: TeacherDashboardHeroModel;
    dayCard: DashboardDayCardContent;
    miniPlan: TeacherDashboardTimelineItemModel[];
    heroSection: DashboardHeroSectionContent;
    featuredStat: TeacherDashboardFeaturedStatModel;
    compactStats: TeacherDashboardCompactStatModel[];
    planItems: TeacherDashboardTimelineItemModel[];
    attentionItems: TeacherDashboardAttentionItem[];
    courses: TeacherDashboardCourseCardModel[];
    activityItems: TeacherDashboardActivityItem[];
    journalRows: TeacherDashboardJournalRowModel[];
    ai: DashboardAiCardContent;
}

export interface TeacherDashboardViewModel {
    shell: DashboardShellConfig;
    calendarContent: DashboardCalendarContent;
    calendarDays: DashboardCalendarDay[];
    notifications: DashboardNotificationsContent;
    notes: DashboardNotesContent;
    profilePanel: DashboardProfilePanelContent;
    createModal: DashboardCreateItemModalContent;
}
