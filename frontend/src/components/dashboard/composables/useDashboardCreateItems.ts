import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import {
    createDashboardItem,
    getDashboardItems,
    removeDashboardItem,
} from "@/components/dashboard/services/dashboard-items.service";
import type {
    DashboardCalendarDay,
    DashboardItemCreatePayload,
    DashboardItemDto,
    DashboardNotesContent,
} from "@/components/dashboard/types/dashboard.types";

interface DashboardCreateItemsViewModel {
    calendarDays: DashboardCalendarDay[];
    notes: DashboardNotesContent;
}

interface DashboardCreateItemsSource {
    value: DashboardCreateItemsViewModel;
}

export function useDashboardCreateItems(
    viewModel: DashboardCreateItemsSource,
) {
    const createModalKind = ref<DashboardItemCreatePayload["kind"]>("calendar");
    const isCreateModalOpen = ref(false);
    const isSaving = ref(false);
    const saveError = ref("");
    const persistedItems = ref<DashboardItemDto[]>([]);
    const persistedNotes = computed(() => {
        return persistedItems.value.filter((item) => item.kind === "note");
    });
    const persistedCalendarItems = computed(() => {
        return persistedItems.value.filter((item) => {
            return item.kind === "calendar" || item.kind === "note";
        });
    });

    const notesContent = computed<DashboardNotesContent>(() => {
        return {
            ...viewModel.value.notes,
            items: [
                ...persistedNotes.value.map((item) => ({
                    id: item.id,
                    itemId: item.id,
                    date: formatShortDate(item.date),
                    title: item.title,
                    text: item.text,
                })),
                ...viewModel.value.notes.items,
            ],
        };
    });

    const calendarDays = computed<DashboardCalendarDay[]>(() => {
        const sourceDays = viewModel.value.calendarDays.map((day) => {
            const createdItemsForDay = persistedCalendarItems.value.filter((item) => {
                return item.date === day.date;
            });

            const latestItem = createdItemsForDay[0];

            if (!latestItem) {
                return day;
            }

            return {
                ...day,
                itemId: latestItem.id,
                title: latestItem.title,
                text: latestItem.text,
                events: [
                    ...(day.events || []),
                    ...createdItemsForDay.map((item) => {
                        return {
                            type: item.kind === "note" ? "neutral" : item.event_type,
                        };
                    }),
                ],
            };
        });

        const existingDates = new Set(sourceDays.map((day) => day.date));

        const syntheticDays = persistedCalendarItems.value
            .filter((item) => {
                return !existingDates.has(item.date);
            })
            .map((item) => {
                const date = parseDateKey(item.date) || new Date();

                return {
                    itemId: item.id,
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
                            type: item.kind === "note" ? "neutral" : item.event_type,
                        },
                    ],
                };
            });

        return [
            ...sourceDays,
            ...syntheticDays,
        ];
    });

    async function loadItems(): Promise<void> {
        try {
            persistedItems.value = await getDashboardItems();
        } catch {
            saveError.value = "Не удалось загрузить сохраненные элементы.";
        }
    }

    function openCreateModal(kind: DashboardItemCreatePayload["kind"]): void {
        saveError.value = "";
        createModalKind.value = kind;
        isCreateModalOpen.value = true;
    }

    function closeCreateModal(): void {
        isCreateModalOpen.value = false;
    }

    async function submitCreateModal(payload: DashboardItemCreatePayload): Promise<boolean> {
        const title = payload.title.trim();
        const text = payload.text.trim();
        const date = payload.date || getTodayDateKey();

        if (!title) {
            return false;
        }

        isSaving.value = true;
        saveError.value = "";

        try {
            const item = await createDashboardItem({
                ...payload,
                title,
                text,
                date,
                eventType: payload.kind === "note" ? "neutral" : payload.eventType,
            });

            persistedItems.value.unshift(item);
            closeCreateModal();

            return true;
        } catch (error) {
            saveError.value = error instanceof Error
                ? error.message
                : "Не удалось сохранить элемент.";

            return false;
        } finally {
            isSaving.value = false;
        }
    }

    async function deleteItem(itemId: number): Promise<boolean> {
        saveError.value = "";

        try {
            await removeDashboardItem(itemId);
            persistedItems.value = persistedItems.value.filter((item) => item.id !== itemId);
            window.dispatchEvent(new Event("dashboard-items:changed"));

            return true;
        } catch (error) {
            saveError.value = error instanceof Error
                ? error.message
                : "Не удалось удалить элемент.";

            return false;
        }
    }

    function handleDashboardItemsChange(): void {
        void loadItems();
    }

    onMounted(() => {
        void loadItems();
        window.addEventListener("dashboard-items:changed", handleDashboardItemsChange);
    });

    onBeforeUnmount(() => {
        window.removeEventListener("dashboard-items:changed", handleDashboardItemsChange);
    });

    return {
        calendarDays,
        createModalKind,
        isCreateModalOpen,
        isSaving,
        notesContent,
        saveError,
        closeCreateModal,
        deleteItem,
        loadItems,
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
