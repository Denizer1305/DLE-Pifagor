import { computed, onMounted, reactive, ref } from "vue";

import {
    createDashboardItem,
    getDashboardItems,
    removeDashboardItem,
} from "@/components/dashboard/services/dashboard-items.service";
import { calendarPageContent } from "@/modules/calendar/data/calendar-page.data";
import { createCalendarPageModel } from "@/modules/calendar/mappers/calendar-page.mapper";
import type {
    DashboardCalendarDay,
    DashboardCalendarEventType,
    DashboardItemDto,
} from "@/components/dashboard/types/dashboard.types";
import { ROLE_LABELS } from "@/app/constants/roles.constants";
import { useAuthStore } from "@/stores/auth.store";

export function useCalendarPage() {
    const authStore = useAuthStore();
    const items = ref<DashboardItemDto[]>([]);
    const isLoading = ref(false);
    const isSaving = ref(false);
    const errorMessage = ref("");
    const saveError = ref("");
    const selectedDate = ref(getTodayDateKey());
    const visibleMonthDate = ref(new Date());

    const form = reactive({
        title: "",
        text: "",
        date: getTodayDateKey(),
        eventType: "lesson" as DashboardCalendarEventType,
        notificationEnabled: true,
    });

    const model = computed(() => {
        return createCalendarPageModel({
            fullName: authStore.userFullName || authStore.user?.email || "",
            roleCode: authStore.activeRole || "",
            roleLabel: authStore.activeRole
                ? ROLE_LABELS[authStore.activeRole]
                : "Пользователь",
            avatarUrl: authStore.avatarUrl || "",
        });
    });

    const calendarItems = computed(() => {
        return items.value.filter((item) => {
            return item.kind === "calendar" || item.kind === "note";
        });
    });

    const monthLabel = computed(() => {
        return new Intl.DateTimeFormat("ru-RU", {
            month: "long",
            year: "numeric",
        }).format(visibleMonthDate.value);
    });

    const displayedDays = computed<DashboardCalendarDay[]>(() => {
        return buildMonthDays(visibleMonthDate.value, calendarItems.value, selectedDate.value);
    });

    const selectedDayItems = computed(() => {
        return calendarItems.value.filter((item) => item.date === selectedDate.value);
    });

    const selectedDateLabel = computed(() => {
        return formatLongDate(selectedDate.value);
    });

    async function loadCalendar(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            items.value = await getDashboardItems();
        } catch (error) {
            errorMessage.value = getErrorMessage(error, "Не удалось загрузить календарь.");
        } finally {
            isLoading.value = false;
        }
    }

    async function submitPlanItem(): Promise<void> {
        const title = form.title.trim();

        if (!title) {
            return;
        }

        isSaving.value = true;
        saveError.value = "";

        try {
            const item = await createDashboardItem({
                kind: "calendar",
                title,
                text: form.text.trim(),
                date: form.date || selectedDate.value || getTodayDateKey(),
                eventType: form.eventType,
                notificationEnabled: form.notificationEnabled,
            });

            items.value = [item, ...items.value];
            selectedDate.value = item.date;
            resetForm(item.date);
            notifyDashboardItemsChanged();
        } catch (error) {
            saveError.value = getErrorMessage(error, "Не удалось сохранить событие.");
        } finally {
            isSaving.value = false;
        }
    }

    async function deletePlanItem(itemId: number): Promise<void> {
        saveError.value = "";

        try {
            await removeDashboardItem(itemId);
            items.value = items.value.filter((item) => item.id !== itemId);
            notifyDashboardItemsChanged();
        } catch (error) {
            saveError.value = getErrorMessage(error, "Не удалось удалить событие.");
        }
    }

    function selectDay(day: DashboardCalendarDay): void {
        selectedDate.value = day.date;
        form.date = day.date;
    }

    function showPreviousMonth(): void {
        visibleMonthDate.value = addMonths(visibleMonthDate.value, -1);
    }

    function showNextMonth(): void {
        visibleMonthDate.value = addMonths(visibleMonthDate.value, 1);
    }

    function selectEventType(value: string): void {
        if (isEventType(value)) {
            form.eventType = value;
        }
    }

    function resetForm(date = selectedDate.value): void {
        form.title = "";
        form.text = "";
        form.date = date || getTodayDateKey();
        form.eventType = "lesson";
        form.notificationEnabled = true;
    }

    onMounted(() => {
        void loadCalendar();
    });

    return {
        content: calendarPageContent,
        displayedDays,
        errorMessage,
        form,
        isLoading,
        isSaving,
        model,
        monthLabel,
        saveError,
        selectedDate,
        selectedDateLabel,
        selectedDayItems,
        deletePlanItem,
        loadCalendar,
        selectDay,
        selectEventType,
        showNextMonth,
        showPreviousMonth,
        submitPlanItem,
    };
}

function buildMonthDays(
    monthDate: Date,
    items: DashboardItemDto[],
    selectedDate: string,
): DashboardCalendarDay[] {
    const year = monthDate.getFullYear();
    const month = monthDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const startOffset = (firstDay.getDay() + 6) % 7;
    const startDate = new Date(year, month, 1 - startOffset);
    const todayKey = getTodayDateKey();

    return Array.from({ length: 42 }, (_, index) => {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + index);

        const dateKey = getDateKey(date);
        const dayItems = items.filter((item) => item.date === dateKey);
        const latestItem = dayItems[0];

        return {
            itemId: latestItem?.id,
            date: dateKey,
            day: date.getDate(),
            dateLabel: formatLongDate(dateKey),
            isToday: dateKey === todayKey,
            isSelected: dateKey === selectedDate,
            isMuted: date.getMonth() !== month,
            isWeekend: date.getDay() === 0 || date.getDay() === 6,
            title: latestItem?.title || "",
            text: latestItem?.text || "",
            events: dayItems.map((item) => ({
                type: item.kind === "note" ? "neutral" : item.event_type,
            })),
        };
    });
}

function isEventType(value: string): value is DashboardCalendarEventType {
    return ["lesson", "checking", "deadline", "system", "neutral"].includes(value);
}

function notifyDashboardItemsChanged(): void {
    window.dispatchEvent(new Event("dashboard-items:changed"));
}

function getErrorMessage(error: unknown, fallback: string): string {
    return error instanceof Error && error.message ? error.message : fallback;
}

function addMonths(value: Date, count: number): Date {
    return new Date(value.getFullYear(), value.getMonth() + count, 1);
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

function formatLongDate(value: string): string {
    const [year, month, day] = value.split("-").map(Number);
    const date = year && month && day ? new Date(year, month - 1, day) : new Date();

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
    }).format(date);
}
