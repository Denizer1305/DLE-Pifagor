import type { DashboardAction } from "@/components/dashboard/types/dashboard.types";

export const dashboardPlanCreateActions: DashboardAction[] = [
    {
        label: "Добавить событие",
        icon: "fas fa-calendar-plus",
        createKind: "calendar",
        variant: "primary",
    },
    {
        label: "Добавить заметку",
        icon: "fas fa-note-sticky",
        createKind: "note",
    },
];
