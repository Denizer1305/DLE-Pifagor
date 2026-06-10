import type { DashboardAiCardContent } from "@/components/dashboard/types/dashboard.types";
import type { TeacherDashboardHeroModel } from "@/modules/teacher/types/teacher-dashboard.types";

import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";

export const teacherDashboardHero: TeacherDashboardHeroModel = {
    badges: [
        {
            label: "Доброе утро",
            icon: "fas fa-sun",
        },
        {
            label: "Рабочее пространство",
            icon: "fas fa-book",
        },
        {
            label: "Проверка заданий",
            icon: "fas fa-clipboard-check",
        },
    ],
    title: "Рабочее пространство преподавателя",
    text:
        "Здесь собраны курсы, занятия, задания, аналитика и всё, что помогает вести образовательный процесс спокойно и структурно.",
    actions: [
        {
            label: "Создать урок",
            icon: "fas fa-plus",
            routeName: "teacher-lessons-create",
            variant: "primary",
        },
        {
            label: "Создать тест",
            icon: "fas fa-file-circle-plus",
            routeName: "teacher-tests-create",
            variant: "secondary",
        },
        {
            label: "Выдать домашнее задание",
            icon: "fas fa-house-laptop",
            routeName: "teacher-homework-create",
            variant: "secondary",
        },
        {
            label: "Открыть журнал",
            icon: "fas fa-table-list",
            routeName: "teacher-journal",
            variant: "secondary",
        },
    ],
};

export const teacherAiCardContent: DashboardAiCardContent = {
    image: {
        src: anastasiaLogo,
        alt: "Анастасия ИИ",
    },
    title: "Анастасия",
    subtitle: "Именной ИИ-помощник преподавателя",
    text:
        "Поможет составить урок, придумать тест, подготовить домашнее задание или подсказать, на что обратить внимание в аналитике группы.",
    action: {
        label: "Открыть Анастасию",
        icon: "fas fa-sparkles",
        to: {
            name: "teacher-dashboard",
        },
        variant: "primary",
    },
};
