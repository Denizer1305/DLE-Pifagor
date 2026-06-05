import { computed, type Ref } from "vue";

import { useDashboardCalendarPlan } from "@/components/dashboard/composables/useDashboardCalendarPlan";
import { teacherDashboardPageUi } from "@/modules/teacher/data/teacher-dashboard.data";
import type { TeacherDashboardPageModel } from "@/modules/teacher/types/teacher-dashboard.types";
import type {
    DashboardCardSectionContent,
    DashboardCourseCardContent,
    DashboardStatsCardContent,
    DashboardTimelineContent,
} from "@/components/dashboard/types/dashboard.types";

export function useTeacherDashboardPresentation(
    pageModel: Ref<TeacherDashboardPageModel>,
) {
    const ui = teacherDashboardPageUi;
    const { calendarPlanItems } = useDashboardCalendarPlan();

    const featuredStatCard = computed<DashboardStatsCardContent>(() => {
        return {
            key: "featured",
            icon: pageModel.value.featuredStat.icon,
            title: pageModel.value.featuredStat.title,
            value: pageModel.value.featuredStat.value,
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
            ...ui.plan,
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

    const attentionContent = computed<DashboardCardSectionContent>(() => {
        return {
            ...ui.attention,
            items: pageModel.value.attentionItems,
        };
    });

    const courseCards = computed<DashboardCourseCardContent[]>(() => {
        return pageModel.value.courses.map((course) => {
            return {
                id: course.id,
                icon: course.icon,
                status: course.status,
                statusVariant: course.statusVariant,
                title: course.title,
                description: course.description,
                meta: [
                    {
                        value: course.modulesCount,
                        label: ui.courses.meta.modules,
                    },
                    {
                        value: course.studentsCount,
                        label: ui.courses.meta.students,
                    },
                ],
                progress: course.progress,
                progressLabel: ui.courses.progressLabel,
                actions: [
                    {
                        label: ui.courses.actions.open,
                        to: {
                            name: "teacher-course-detail",
                            params: { id: course.id },
                        },
                        variant: "primary",
                    },
                    {
                        label: ui.courses.actions.edit,
                        to: {
                            name: "teacher-course-edit",
                            params: { id: course.id },
                        },
                    },
                    {
                        label: ui.courses.actions.analytics,
                        to: {
                            name: "teacher-course-analytics",
                            params: { id: course.id },
                        },
                    },
                ],
            };
        });
    });

    const activityContent = computed<DashboardCardSectionContent>(() => {
        return {
            ...ui.activity,
            items: pageModel.value.activityItems,
        };
    });

    const journalRows = computed(() => {
        return pageModel.value.journalRows.map((row) => {
            return {
                id: row.id,
                cells: [row.student, row.work, row.grade],
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
        attentionContent,
        courseCards,
        activityContent,
        journalRows,
    };
}
