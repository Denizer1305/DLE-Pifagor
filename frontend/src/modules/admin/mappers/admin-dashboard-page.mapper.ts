import { adminAiCardContent } from "@/modules/admin/data/admin-dashboard.data";
import {
    mapAdminDayCard,
    mapAdminHero,
    mapCalendarToPlanItems,
} from "@/modules/admin/mappers/admin-dashboard-page-hero.mapper";
import {
    mapAdminCompactStats,
    mapAdminCriticalItems,
    mapAdminFeaturedStat,
    mapAdminOverviewRows,
} from "@/modules/admin/mappers/admin-dashboard-page-metrics.mapper";
import {
    mapAdminParticipants,
    mapAdminRecentEvents,
} from "@/modules/admin/mappers/admin-dashboard-page-participants.mapper";
import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";
import type { AdminDashboardPageModel } from "@/modules/admin/types/admin-dashboard-page.types";

export function mapAdminSummaryToPageModel(
    summary: AdminDashboardSummary,
): AdminDashboardPageModel {
    const hero = mapAdminHero(summary);
    const dayCard = mapAdminDayCard(summary);
    const planItems = mapCalendarToPlanItems(summary);
    const miniPlan = planItems.slice(0, 3);

    return {
        hero,
        dayCard,
        miniPlan,
        heroSection: {
            hero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайший план",
            miniPlanIcon: "fas fa-clock",
            miniPlanEmptyText: "План пока не заполнен. Добавьте событие или заметку в календаре.",
        },
        featuredStat: mapAdminFeaturedStat(summary),
        compactStats: mapAdminCompactStats(summary),
        planItems,
        criticalItems: mapAdminCriticalItems(summary),
        participants: mapAdminParticipants(summary),
        recentEvents: mapAdminRecentEvents(summary),
        overviewRows: mapAdminOverviewRows(summary),
        ai: adminAiCardContent,
    };
}
