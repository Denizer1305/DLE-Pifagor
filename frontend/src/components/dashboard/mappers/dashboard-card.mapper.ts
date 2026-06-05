import type {
    DashboardCardSectionContent,
    DashboardListItem,
    DashboardTimelineContent,
    DashboardTimelineItem,
} from "@/components/dashboard/types/dashboard.types";

interface DashboardSectionSource {
    badge?: string;
    icon?: string;
    title: string;
    text?: string;
    emptyText?: string;
}

interface DashboardGradeRowSource {
    id: string | number;
    subject: string;
    work: string;
    grade: string;
    status: string;
    warning?: boolean;
}

export function createDashboardCardSectionContent(
    section: DashboardSectionSource,
    items: DashboardListItem[],
): DashboardCardSectionContent {
    return {
        badge: section.badge,
        icon: section.icon,
        title: section.title,
        text: section.text,
        emptyText: section.emptyText,
        items,
    };
}

export function createDashboardTimelineContent(
    section: DashboardSectionSource,
    items: DashboardTimelineItem[],
): DashboardTimelineContent {
    return {
        badge: section.badge,
        icon: section.icon,
        title: section.title,
        text: section.text,
        emptyText: section.emptyText,
        items,
    };
}

export function mapDashboardGradeRows(rows: DashboardGradeRowSource[]) {
    return rows.map((row) => {
        return {
            id: row.id,
            cells: [row.subject, row.work, row.grade],
            status: row.status,
            warning: row.warning,
        };
    });
}
