type CalendarButton = HTMLButtonElement;

interface CalendarDayHandler {
    button: CalendarButton;
    handler: EventListener;
}

function getById<T extends HTMLElement>(id: string): T | null {
    return document.getElementById(id) as T | null;
}

function resolveBadgeText(button: CalendarButton): string {
    return button.dataset.badgeLabel || "";
}

export function useDashboardMiniCalendar() {
    let calendarDays: CalendarButton[] = [];
    let calendarDayHandlers: CalendarDayHandler[] = [];
    let calendarRoot: HTMLElement | null = null;

    function init(): void {
        if (typeof document === "undefined") {
            return;
        }

        calendarRoot =
            getById("teacherMiniCalendar") ||
            getById("studentMiniCalendar") ||
            getById("parentMiniCalendar") ||
            getById("adminMiniCalendar");

        const isAdminCalendar = calendarRoot?.id === "adminMiniCalendar";
        const noteDate = getById(isAdminCalendar ? "adminCalendarNoteDate" : "dashboardCalendarNoteDate");
        const noteTitle = getById(isAdminCalendar ? "adminCalendarNoteTitle" : "dashboardCalendarNoteTitle");
        const noteText = getById(isAdminCalendar ? "adminCalendarNoteText" : "dashboardCalendarNoteText");
        const noteBadge = getById("dashboardCalendarNoteBadge");

        if (!calendarRoot || !noteDate || !noteTitle || !noteText) {
            return;
        }

        calendarDays = Array.from(
            calendarRoot.querySelectorAll<CalendarButton>(".dashboard-calendar-day"),
        );

        if (!calendarDays.length) {
            return;
        }

        const setActiveDay = (button: CalendarButton): void => {
            calendarDays.forEach((day) => {
                day.classList.remove("is-selected");
            });

            button.classList.add("is-selected");

            noteDate.textContent = button.dataset.dateLabel || "";
            noteTitle.textContent = button.dataset.noteTitle || "";
            noteText.textContent = button.dataset.noteText || "";

            if (noteBadge) {
                noteBadge.textContent = resolveBadgeText(button);
            }
        };

        calendarDays.forEach((button) => {
            const handler = (): void => {
                if (isAdminCalendar) {
                    const wasToday = button.classList.contains("is-today");

                    calendarDays.forEach((day) => {
                        if (day !== button && day.dataset.day !== "14") {
                            day.classList.remove("is-today");
                        }
                    });

                    if (wasToday) {
                        button.classList.add("is-today");
                    }
                }

                setActiveDay(button);
            };

            button.addEventListener("click", handler);
            calendarDayHandlers.push({ button, handler });
        });
    }

    function destroy(): void {
        calendarDayHandlers.forEach(({ button, handler }) => {
            button.removeEventListener("click", handler);
        });

        calendarRoot = null;
        calendarDays = [];
        calendarDayHandlers = [];
    }

    return {
        destroy,
        init,
    };
}
