import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import { dashboardCreateModalContent } from "@/components/dashboard/data/dashboard-create-modal.data";
import { getDashboardItems } from "@/components/dashboard/services/dashboard-items.service";
import type {
    DashboardCalendarEventType,
    DashboardItemDto,
    DashboardTimelineItem,
} from "@/components/dashboard/types/dashboard.types";

const DASHBOARD_ITEMS_CHANGED_EVENT = "dashboard-items:changed";

export function useDashboardCalendarPlan() {
    const items = ref<DashboardItemDto[]>([]);

    const calendarPlanItems = computed<DashboardTimelineItem[]>(() => {
        const todayKey = getTodayDateKey();

        return items.value
            .filter((item) => item.kind === "calendar" && item.date >= todayKey)
            .sort(compareCalendarItems)
            .slice(0, 6)
            .map((item) => {
                return {
                    id: `calendar-${item.id}`,
                    time: formatTimelineDate(item.date),
                    title: item.title,
                    text: item.text || getEventTypeLabel(item.event_type),
                    tone: getEventTone(item.event_type),
                };
            });
    });

    async function loadCalendarPlan(): Promise<void> {
        try {
            items.value = await getDashboardItems();
        } catch {
            items.value = [];
        }
    }

    function handleDashboardItemsChange(): void {
        void loadCalendarPlan();
    }

    onMounted(() => {
        void loadCalendarPlan();
        window.addEventListener(DASHBOARD_ITEMS_CHANGED_EVENT, handleDashboardItemsChange);
    });

    onBeforeUnmount(() => {
        window.removeEventListener(DASHBOARD_ITEMS_CHANGED_EVENT, handleDashboardItemsChange);
    });

    return {
        calendarPlanItems,
        loadCalendarPlan,
    };
}

function compareCalendarItems(first: DashboardItemDto, second: DashboardItemDto): number {
    const dateCompare = first.date.localeCompare(second.date);

    if (dateCompare !== 0) {
        return dateCompare;
    }

    return second.created_at.localeCompare(first.created_at);
}

function getEventTypeLabel(type: DashboardCalendarEventType): string {
    return dashboardCreateModalContent.calendarEventThemeOptions.find((option) => {
        return option.value === type;
    })?.label || "Событие календаря";
}

function getEventTone(type: DashboardCalendarEventType): DashboardTimelineItem["tone"] {
    if (type === "deadline") {
        return "warning";
    }

    if (type === "system") {
        return "danger";
    }

    if (type === "checking") {
        return "primary";
    }

    return undefined;
}

function getTodayDateKey(): string {
    return getDateKey(new Date());
}

function getDateKey(value: Date): string {
    return [
        value.getFullYear(),
        String(value.getMonth() + 1).padStart(2, "0"),
        String(value.getDate()).padStart(2, "0"),
    ].join("-");
}

function formatTimelineDate(value: string): string {
    const [year, month, day] = value.split("-").map(Number);

    if (!year || !month || !day) {
        return value;
    }

    const date = new Date(year, month - 1, day);

    if (value === getTodayDateKey()) {
        return "Сегодня";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
    }).format(date);
}
