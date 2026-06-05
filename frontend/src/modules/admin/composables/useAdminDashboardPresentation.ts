import { computed, type ComputedRef } from "vue";

import { useDashboardCalendarPlan } from "@/components/dashboard/composables/useDashboardCalendarPlan";
import { adminDashboardPageUi } from "@/modules/admin/data/admin-dashboard-page.data";
import type { AdminDashboardPageModel } from "@/modules/admin/types/admin-dashboard-page.types";
import type {
    DashboardCardSectionContent,
    DashboardCourseCardContent,
    DashboardStatsCardContent,
    DashboardTimelineContent,
} from "@/components/dashboard/types/dashboard.types";

export function useAdminDashboardPresentation(
    pageModel: ComputedRef<AdminDashboardPageModel>,
) {
    const ui = adminDashboardPageUi;
    const { calendarPlanItems } = useDashboardCalendarPlan();

    const featuredStatCard = computed<DashboardStatsCardContent>(() => {
        return {
            key: "featured",
            icon: pageModel.value.featuredStat.icon,
            title: pageModel.value.featuredStat.title,
            value: `${pageModel.value.featuredStat.value}%`,
            text: pageModel.value.featuredStat.label,
            progress: pageModel.value.featuredStat.progress,
        };
    });

    const compactStatCards = computed<DashboardStatsCardContent[]>(() => {
        return pageModel.value.compactStats.map((stat) => {
            return {
                key: stat.key,
                icon: stat.icon,
                title: stat.title,
                value: stat.value,
                text: stat.text,
            };
        });
    });

    const planContent = computed<DashboardTimelineContent>(() => {
        return {
            badge: pageModel.value.dayCard.title,
            icon: ui.plan.icon,
            title: ui.plan.title,
            text: ui.plan.text,
            emptyText: ui.plan.emptyText,
            items: [
                ...calendarPlanItems.value,
                ...pageModel.value.planItems.map((item) => {
                    return {
                        id: `${item.time}-${item.title}`,
                        time: item.time,
                        title: item.title,
                        text: item.text,
                    };
                }),
            ],
        };
    });

    const criticalContent = computed<DashboardCardSectionContent>(() => {
        return {
            ...ui.critical,
            items: pageModel.value.criticalItems.map((item) => {
                return {
                    id: item.title,
                    icon: item.icon,
                    title: item.title,
                    text: item.text,
                };
            }),
        };
    });

    const participantCards = computed<DashboardCourseCardContent[]>(() => {
        return pageModel.value.participants.map((participant) => {
            return {
                id: participant.title,
                icon: participant.icon,
                status: participant.status,
                statusVariant: "active",
                title: participant.title,
                description: participant.text,
                meta: [
                    {
                        value: participant.firstValue,
                        label: participant.firstLabel,
                    },
                    {
                        value: participant.secondValue,
                        label: participant.secondLabel,
                    },
                ],
                progress: participant.progress,
                progressLabel: participant.progressLabel,
                actions: participant.actions.map((action, index) => {
                    return {
                        label: action,
                        href: "#",
                        variant: index === 0 ? "primary" : "secondary",
                    };
                }),
            };
        });
    });

    const recentEventsContent = computed<DashboardCardSectionContent>(() => {
        return {
            ...ui.events,
            items: pageModel.value.recentEvents.map((event) => {
                return {
                    id: event.title,
                    icon: event.icon,
                    title: event.title,
                    text: event.text,
                };
            }),
        };
    });

    const overviewRows = computed(() => {
        return pageModel.value.overviewRows.map((row) => {
            return {
                id: row.section,
                cells: [row.section, row.state, row.value],
                status: row.status,
                warning: row.warning,
            };
        });
    });

    return {
        ui,
        featuredStatCard,
        compactStatCards,
        planContent,
        criticalContent,
        participantCards,
        recentEventsContent,
        overviewRows,
    };
}
