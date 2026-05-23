import { computed, ref } from "vue";

import type {
    DashboardCalendarDay,
    DashboardCalendarEventType,
    DashboardCreateItemKind,
    DashboardNotesContent,
} from "@/components/dashboard/types/dashboard.types";

interface DashboardCreateItemsViewModel {
    calendarDays: DashboardCalendarDay[];
    notes: DashboardNotesContent;
}

interface DashboardCreateItemsSource {
    value: DashboardCreateItemsViewModel;
}

interface DashboardCreateItemPayload {
    kind: DashboardCreateItemKind;
    title: string;
    text: string;
    date: string;
    eventType: DashboardCalendarEventType;
}

interface CreatedNoteItem {
    id: string;
    date: string;
    title: string;
    text: string;
}

interface CreatedCalendarItem {
    id: string;
    date: string;
    title: string;
    text: string;
    eventType: DashboardCalendarEventType;
}

export function useDashboardCreateItems(
    viewModel: DashboardCreateItemsSource,
) {
    const createModalKind = ref<DashboardCreateItemKind>("calendar");
    const isCreateModalOpen = ref(false);

    const createdNotes = ref<CreatedNoteItem[]>([]);
    const createdCalendarItems = ref<CreatedCalendarItem[]>([]);

    const notesContent = computed<DashboardNotesContent>(() => {
        return {
            ...viewModel.value.notes,
            items: [
                ...createdNotes.value,
                ...viewModel.value.notes.items,
            ],
        };
    });

    const calendarDays = computed<DashboardCalendarDay[]>(() => {
        const sourceDays = viewModel.value.calendarDays.map((day) => {
            const createdItemsForDay = createdCalendarItems.value.filter((item) => {
                return item.date === day.date;
            });

            const latestItem = createdItemsForDay[0];

            if (!latestItem) {
                return day;
            }

            return {
                ...day,
                title: latestItem.title,
                text: latestItem.text,
                events: [
                    ...(day.events || []),
                    ...createdItemsForDay.map((item) => {
                        return {
                            type: item.eventType,
                        };
                    }),
                ],
            };
        });

        const existingDates = new Set(sourceDays.map((day) => day.date));

        const syntheticDays = createdCalendarItems.value
            .filter((item) => {
                return !existingDates.has(item.date);
            })
            .map((item) => {
                const date = parseDateKey(item.date) || new Date();

                return {
                    date: item.date,
                    day: date.getDate(),
                    dateLabel: formatCalendarDateLabel(item.date),
                    isToday: item.date === getTodayDateKey(),
                    isSelected: false,
                    isMuted: false,
                    isWeekend: date.getDay() === 0 || date.getDay() === 6,
                    title: item.title,
                    text: item.text,
                    events: [
                        {
                            type: item.eventType,
                        },
                    ],
                };
            });

        return [
            ...sourceDays,
            ...syntheticDays,
        ];
    });

    function openCreateModal(kind: DashboardCreateItemKind): void {
        createModalKind.value = kind;
        isCreateModalOpen.value = true;
    }

    function closeCreateModal(): void {
        isCreateModalOpen.value = false;
    }

    function submitCreateModal(payload: DashboardCreateItemPayload): void {
        const title = payload.title.trim();
        const text = payload.text.trim();
        const date = payload.date || getTodayDateKey();

        if (!title) {
            return;
        }

        if (payload.kind === "note") {
            createdNotes.value.unshift({
                id: `note-${Date.now()}`,
                date: formatShortDate(date),
                title,
                text,
            });

            closeCreateModal();
            return;
        }

        createdCalendarItems.value.unshift({
            id: `calendar-${Date.now()}`,
            date,
            title,
            text,
            eventType: payload.eventType,
        });

        closeCreateModal();
    }

    return {
        calendarDays,
        createModalKind,
        isCreateModalOpen,
        notesContent,
        closeCreateModal,
        openCreateModal,
        submitCreateModal,
    };
}

function getTodayDateKey(): string {
    const today = new Date();

    return [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0"),
    ].join("-");
}

function parseDateKey(value: string): Date | null {
    if (!value) {
        return null;
    }

    const [year, month, day] = value.split("-").map(Number);

    if (!year || !month || !day) {
        return null;
    }

    return new Date(year, month - 1, day);
}

function formatShortDate(value: string): string {
    const date = parseDateKey(value);

    if (!date) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "2-digit",
        month: "short",
    }).format(date);
}

function formatCalendarDateLabel(value: string): string {
    const date = parseDateKey(value);

    if (!date) {
        return "";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
    }).format(date);
}
