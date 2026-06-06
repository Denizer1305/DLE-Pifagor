import { computed, type Ref } from "vue";

import { dashboardPlanCreateActions } from "@/components/dashboard/data/dashboard-plan-actions.data";
import { useDashboardCalendarPlan } from "@/components/dashboard/composables/useDashboardCalendarPlan";
import {
    createDashboardCardSectionContent,
    createDashboardTimelineContent,
    mapDashboardGradeRows,
} from "@/components/dashboard/mappers/dashboard-card.mapper";
import { studentDashboardPageUi } from "@/modules/student/data/student-dashboard.data";
import type { StudentDashboardModel } from "@/modules/student/types/student-dashboard.types";

export function useStudentDashboardPresentation(
    model: Ref<StudentDashboardModel>,
) {
    const ui = studentDashboardPageUi;
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

    const assignmentsContent = computed(() => {
        return createDashboardCardSectionContent(
            model.value.assignmentsSection,
            model.value.assignments,
        );
    });

    const activityContent = computed(() => {
        return createDashboardCardSectionContent(
            model.value.activitySection,
            model.value.activityItems,
        );
    });

    const goalsContent = computed(() => {
        return createDashboardCardSectionContent(
            model.value.goalsSection,
            model.value.goals,
        );
    });

    const gradeRows = computed(() => {
        return mapDashboardGradeRows(model.value.gradeRows);
    });

    return {
        ui,
        scheduleContent,
        assignmentsContent,
        activityContent,
        goalsContent,
        gradeRows,
    };
}
