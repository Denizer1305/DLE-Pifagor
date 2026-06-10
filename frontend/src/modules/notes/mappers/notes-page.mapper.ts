import {
    createCalendarPageModel,
    type CalendarUserContext,
} from "@/modules/calendar/mappers/calendar-page.mapper";
import type {
    DashboardItemDto,
    DashboardPageScaffoldModel,
} from "@/components/dashboard/types/dashboard.types";

export interface NotesPageStats {
    total: number;
    upcoming: number;
    today: number;
}

export interface NotesPageNote {
    id: number;
    title: string;
    text: string;
    previewText: string;
    hasLongText: boolean;
    date: string;
    dateLabel: string;
    isToday: boolean;
    isPast: boolean;
}

export function createNotesPageModel(
    context: CalendarUserContext,
): DashboardPageScaffoldModel {
    const model = createCalendarPageModel(context);

    return {
        ...model,
        shell: {
            ...model.shell,
            pageClass: `${model.shell.pageClass} notes-page`,
            search: {
                placeholder: "Поиск по заметкам, датам и напоминаниям...",
                ariaLabel: "Поиск по заметкам",
            },
        },
    };
}

export function mapNotesPageItems(items: DashboardItemDto[]): NotesPageNote[] {
    return items
        .filter((item) => item.kind === "note")
        .map((item) => {
            return {
                id: item.id,
                title: item.title,
                text: item.text,
                previewText: createPreviewText(item.text),
                hasLongText: item.text.trim().length > NOTE_PREVIEW_LIMIT,
                date: item.date,
                dateLabel: formatLongDate(item.date),
                isToday: item.date === getTodayDateKey(),
                isPast: item.date < getTodayDateKey(),
            };
        })
        .sort((current, next) => {
            if (current.date === next.date) {
                return next.id - current.id;
            }

            return current.date.localeCompare(next.date);
        });
}

const NOTE_PREVIEW_LIMIT = 220;

function createPreviewText(value: string): string {
    const text = value.trim();

    if (text.length <= NOTE_PREVIEW_LIMIT) {
        return text;
    }

    return `${text.slice(0, NOTE_PREVIEW_LIMIT).trim()}...`;
}

export function mapNotesPageStats(notes: NotesPageNote[]): NotesPageStats {
    const today = getTodayDateKey();

    return {
        total: notes.length,
        upcoming: notes.filter((note) => note.date >= today).length,
        today: notes.filter((note) => note.date === today).length,
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

function formatLongDate(value: string): string {
    const [year, month, day] = value.split("-").map(Number);
    const date = year && month && day ? new Date(year, month - 1, day) : new Date();

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
    }).format(date);
}
