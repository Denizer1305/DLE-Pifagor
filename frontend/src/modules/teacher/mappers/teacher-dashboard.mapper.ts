import {
    createTeacherDayCard,
    teacherAiCardContent,
    teacherDashboardHero,
} from "@/modules/teacher/data/teacher-dashboard.data";
import type {
    TeacherDashboardActivityItem,
    TeacherDashboardActivityItemDto,
    TeacherDashboardAttentionItem,
    TeacherDashboardAttentionItemDto,
    TeacherDashboardCalendarDayDto,
    TeacherDashboardCourse,
    TeacherDashboardCourseCardModel,
    TeacherDashboardCourseDto,
    TeacherDashboardJournalRow,
    TeacherDashboardJournalRowDto,
    TeacherDashboardPageModel,
    TeacherDashboardProfile,
    TeacherDashboardProfileDto,
    TeacherDashboardScheduleItem,
    TeacherDashboardScheduleItemDto,
    TeacherDashboardStat,
    TeacherDashboardStatDto,
    TeacherDashboardSummary,
    TeacherDashboardSummaryDto,
    TeacherDashboardTimelineItemModel,
} from "@/modules/teacher/types/teacher-dashboard.types";
import type { DashboardCalendarDay } from "@/components/dashboard/types/dashboard.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

export function mapTeacherDashboardSummary(
    dto: TeacherDashboardSummaryDto,
): TeacherDashboardSummary {
    return {
        profile: mapProfile(dto.profile),
        stats: dto.stats.map(mapStat),
        schedule: dto.schedule.map(mapScheduleItem),
        calendar: {
            monthLabel: dto.calendar.month_label,
            selectedDate: dto.calendar.selected_date,
            days: dto.calendar.days.map(mapCalendarDay),
        },
        courses: dto.courses.map(mapCourse),
        attentionItems: dto.attention_items.map(mapAttentionItem),
        activityItems: dto.activity_items.map(mapActivityItem),
        journalRows: dto.journal_rows.map(mapJournalRow),
        notifications: dto.notifications,
        notes: dto.notes,
    };
}

export function mapTeacherSummaryToPageModel(
    summary: TeacherDashboardSummary,
): TeacherDashboardPageModel {
    const hero = {
        ...teacherDashboardHero,
        badges: [
            {
                label: "Доброе утро",
                icon: "fas fa-sun",
            },
            {
                label: `${getStatValue(summary, "courses")} активных курсов`,
                icon: "fas fa-book",
            },
            {
                label: `${getStatValue(summary, "checking")} работ на проверке`,
                icon: "fas fa-clipboard-check",
            },
        ],
    };

    const dayCard = createTeacherDayCard(summary);
    const miniPlan = summary.schedule.slice(0, 3).map(mapScheduleToTimeline);

    return {
        hero,
        dayCard,
        miniPlan,
        heroSection: {
            hero,
            dayCard,
            miniPlan,
            miniPlanTitle: "Ближайшее расписание",
            miniPlanIcon: "fas fa-clock",
        },
        featuredStat: {
            icon: "fas fa-chart-column",
            title: "Средняя посещаемость",
            value: `${getStatValue(summary, "attendance")}%`,
            label: "Общий показатель по активным группам за последние 14 дней.",
            progress: Number(getStatValue(summary, "attendance")) || 0,
        },
        compactStats: [
            {
                key: "courses",
                icon: "fas fa-book-open",
                title: "Активные курсы",
                value: getStatValue(summary, "courses"),
                text: "Курсы, которые сейчас находятся в работе.",
            },
            {
                key: "groups",
                icon: "fas fa-users",
                title: "Группы",
                value: getStatValue(summary, "groups"),
                text: "Учебные группы, закреплённые за вами.",
            },
            {
                key: "checking",
                icon: "fas fa-clipboard-check",
                title: "Работы на проверке",
                value: getStatValue(summary, "checking"),
                text: "Ответы и домашние задания, ожидающие проверки.",
            },
            {
                key: "average_grade",
                icon: "fas fa-star",
                title: "Средний балл",
                value: getStatValue(summary, "average_grade"),
                text: "Средний результат учащихся по последним заданиям.",
            },
            {
                key: "homework_done",
                icon: "fas fa-house-laptop",
                title: "Домашние задания",
                value: `${getStatValue(summary, "homework_done")}%`,
                text: "Процент вовремя выполненных домашних работ.",
            },
        ],
        planItems: summary.schedule.map(mapScheduleToTimeline),
        attentionItems: summary.attentionItems,
        courses: summary.courses.map(mapCourseToCard),
        activityItems: summary.activityItems,
        journalRows: summary.journalRows.map((row) => {
            return {
                id: row.id,
                student: row.studentName,
                work: row.workTitle,
                grade: row.grade,
                status: row.status,
                warning: row.isWarning,
            };
        }),
        ai: teacherAiCardContent,
    };
}

function mapProfile(dto: TeacherDashboardProfileDto): TeacherDashboardProfile {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        avatarUrl: resolveBackendAssetUrl(dto.avatar_url),
        roleLabel: dto.role_label,
        subjectLabel: dto.subject_label,
    };
}

function mapStat(dto: TeacherDashboardStatDto): TeacherDashboardStat {
    return {
        key: dto.key,
        label: dto.label,
        value: dto.value,
        caption: dto.caption,
        icon: dto.icon,
        progress: dto.progress,
        tone: dto.tone || "primary",
    };
}

function mapScheduleItem(dto: TeacherDashboardScheduleItemDto): TeacherDashboardScheduleItem {
    return {
        id: dto.id,
        time: dto.time,
        title: dto.title,
        text: dto.text,
        icon: dto.icon || "fas fa-calendar-check",
    };
}

function mapCalendarDay(dto: TeacherDashboardCalendarDayDto): DashboardCalendarDay {
    return {
        date: dto.date,
        day: dto.day,
        dateLabel: dto.date_label || formatCalendarDateLabel(dto.date),
        isToday: dto.is_today,
        isSelected: dto.is_selected,
        isMuted: dto.is_muted,
        isWeekend: dto.is_weekend,
        title: dto.title,
        text: dto.text,
        events: dto.event_types.map((type) => {
            return {
                type: normalizeCalendarEventType(type),
            };
        }),
    };
}

function mapCourse(dto: TeacherDashboardCourseDto): TeacherDashboardCourse {
    return {
        id: dto.id,
        title: dto.title,
        description: dto.description,
        icon: dto.icon,
        status: dto.status,
        statusLabel: dto.status_label,
        modulesCount: dto.modules_count,
        studentsCount: dto.students_count,
        progress: dto.progress,
    };
}

function mapAttentionItem(dto: TeacherDashboardAttentionItemDto): TeacherDashboardAttentionItem {
    return {
        id: dto.id,
        icon: dto.icon,
        title: dto.title,
        text: dto.text,
        tone: dto.tone || "warning",
    };
}

function mapActivityItem(dto: TeacherDashboardActivityItemDto): TeacherDashboardActivityItem {
    return {
        id: dto.id,
        icon: dto.icon,
        title: dto.title,
        text: dto.text,
        tone: dto.tone || "primary",
    };
}

function mapJournalRow(dto: TeacherDashboardJournalRowDto): TeacherDashboardJournalRow {
    return {
        id: dto.id,
        studentName: dto.student_name,
        workTitle: dto.work_title,
        grade: dto.grade,
        status: dto.status,
        isWarning: dto.is_warning,
    };
}

function mapScheduleToTimeline(
    item: TeacherDashboardScheduleItem,
): TeacherDashboardTimelineItemModel {
    return {
        time: item.time,
        title: item.title,
        text: item.text,
    };
}

function mapCourseToCard(course: TeacherDashboardCourse): TeacherDashboardCourseCardModel {
    return {
        id: course.id,
        icon: course.icon,
        title: course.title,
        description: course.description,
        status: course.statusLabel,
        statusVariant: course.status === "active"
            ? "active"
            : course.status === "draft"
                ? "draft"
                : "warning",
        modulesCount: course.modulesCount,
        studentsCount: course.studentsCount,
        progress: course.progress,
    };
}

function getStatValue(
    summary: TeacherDashboardSummary,
    key: string,
): string | number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}

function normalizeCalendarEventType(type: string) {
    if (type === "lesson" || type === "checking" || type === "deadline") {
        return type;
    }

    return "neutral";
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
