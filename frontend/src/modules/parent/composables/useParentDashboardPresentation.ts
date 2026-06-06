import { computed, type Ref } from "vue";

import { dashboardPlanCreateActions } from "@/components/dashboard/data/dashboard-plan-actions.data";
import { useDashboardCalendarPlan } from "@/components/dashboard/composables/useDashboardCalendarPlan";
import {
    createDashboardCardSectionContent,
    createDashboardTimelineContent,
    mapDashboardGradeRows,
} from "@/components/dashboard/mappers/dashboard-card.mapper";
import { parentDashboardPageUi } from "@/modules/parent/data/parent-dashboard.data";
import type { ParentDashboardModel } from "@/modules/parent/types/parent-dashboard.types";

export function useParentDashboardPresentation(
    model: Ref<ParentDashboardModel>,
) {
    const ui = parentDashboardPageUi;
    const { calendarPlanItems } = useDashboardCalendarPlan();

    const scheduleContent = computed(() => {
        const content = createDashboardTimelineContent(
            model.value.scheduleSection,
            model.value.schedule,
        );

        return {
            ...content,
            actions: dashboardPlanCreateActions,
            items: [
                ...calendarPlanItems.value,
                ...content.items,
            ],
        };
    });

    const importantContent = computed(() => {
        return createDashboardCardSectionContent(
            model.value.notificationsSection,
            model.value.importantItems,
        );
    });

    const activityContent = computed(() => {
        return createDashboardCardSectionContent(
            model.value.activitySection,
            model.value.activityItems,
        );
    });

    const messagesContent = computed(() => {
        return createDashboardCardSectionContent(
            model.value.messagesSection,
            model.value.messages,
        );
    });

    const gradeRows = computed(() => {
        return mapDashboardGradeRows(model.value.gradeRows);
    });

    return {
        ui,
        scheduleContent,
        importantContent,
        activityContent,
        messagesContent,
        gradeRows,
    };
}
