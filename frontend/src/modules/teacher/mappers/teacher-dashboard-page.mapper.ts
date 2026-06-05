import {
    createTeacherDayCard,
    teacherAiCardContent,
    teacherDashboardHero,
} from "@/modules/teacher/data/teacher-dashboard.data";
import type {
    TeacherDashboardCourse,
    TeacherDashboardCourseCardModel,
    TeacherDashboardPageModel,
    TeacherDashboardScheduleItem,
    TeacherDashboardSummary,
    TeacherDashboardTimelineItemModel,
} from "@/modules/teacher/types/teacher-dashboard.types";

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

function getStatValue(summary: TeacherDashboardSummary, key: string): string | number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}
