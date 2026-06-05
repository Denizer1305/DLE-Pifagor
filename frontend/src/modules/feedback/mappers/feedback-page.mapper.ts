import {
    createCalendarPageModel,
    type CalendarUserContext,
} from "@/modules/calendar/mappers/calendar-page.mapper";
import type { DashboardPageScaffoldModel } from "@/components/dashboard/types/dashboard.types";

export function createFeedbackPageModel(
    context: CalendarUserContext,
): DashboardPageScaffoldModel {
    const model = createCalendarPageModel(context);

    return {
        ...model,
        shell: {
            ...model.shell,
            pageClass: `${model.shell.pageClass} feedback-page`,
            brand: {
                ...model.shell.brand,
                subtitle: "Обращения и поддержка",
            },
            search: {
                placeholder: "Поиск по обращениям, темам и поддержке...",
                ariaLabel: "Поиск по обращениям",
            },
            sidebarExtra: {
                variant: model.shell.sidebarExtra?.variant || "ai",
                icon: model.shell.sidebarExtra?.icon,
                image: model.shell.sidebarExtra?.image,
                title: "Поддержка",
                subtitle: "Помощь по платформе",
                text: "Опишите вопрос или ошибку, а команда платформы поможет разобраться.",
                action: {
                    label: "На главную",
                    icon: "fas fa-house",
                    to: model.shell.sidebarExtra?.action?.to || { name: "student-dashboard" },
                },
            },
        },
    };
}
