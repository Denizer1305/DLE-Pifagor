import type {
    AdminRoleSettingsDto,
    GuardianRoleSettingsDto,
    LearnerRoleSettingsDto,
    SettingsRoleCode,
    TeacherRoleSettingsDto,
} from "@/modules/settings/types/settings.types";

interface RoleOption {
    key: SettingsRoleCode;
    icon: string;
    label: string;
}

interface RoleToggleOption<TKey extends string> {
    key: TKey;
    label: string;
    text: string;
}

export const settingsRoleOptions: RoleOption[] = [
    {
        key: "teacher",
        icon: "fas fa-chalkboard-user",
        label: "Преподаватель",
    },
    {
        key: "learner",
        icon: "fas fa-user-graduate",
        label: "Студент",
    },
    {
        key: "guardian",
        icon: "fas fa-people-roof",
        label: "Родитель",
    },
    {
        key: "admin",
        icon: "fas fa-user-shield",
        label: "Администратор",
    },
];

export const settingsRoleTitles: Record<SettingsRoleCode, string> = {
    teacher: "Настройки преподавателя",
    learner: "Настройки студента",
    guardian: "Настройки родителя",
    admin: "Настройки администратора",
};

export const teacherRoleOptions: RoleToggleOption<keyof TeacherRoleSettingsDto>[] = [
    {
        key: "show_hero_block",
        label: "Показывать hero-блок кабинета",
        text: "Стартовый блок с приветствием, метриками и быстрыми действиями.",
    },
    {
        key: "show_topbar",
        label: "Показывать верхнюю панель",
        text: "Строка поиска, уведомления и меню профиля.",
    },
    {
        key: "show_sidebar",
        label: "Показывать боковую навигацию",
        text: "Основная навигация по личному кабинету.",
    },
    {
        key: "show_quick_overview",
        label: "Показывать быстрый обзор",
        text: "Краткая сводка по занятиям, заданиям и событиям.",
    },
    {
        key: "show_profile_contacts",
        label: "Показывать контакты в профиле",
        text: "Блок контактов и цифровых каналов связи.",
    },
    {
        key: "show_profile_role_section",
        label: "Показывать ролевую секцию профиля",
        text: "Профессиональные и учебные данные активной роли.",
    },
    {
        key: "show_sidebar_ai",
        label: "Показывать AI в sidebar",
        text: "Блок помощника «Анастасия» в боковой панели.",
    },
    {
        key: "show_ai_card",
        label: "Показывать AI-карточку",
        text: "Отдельная карточка с рекомендациями помощника.",
    },
    {
        key: "show_lesson_hints",
        label: "Подсказки по урокам",
        text: "Рекомендации по материалам, урокам и структуре курса.",
    },
    {
        key: "show_group_analytics",
        label: "Аналитика групп",
        text: "Показ быстрых метрик по закреплённым группам.",
    },
];

export const learnerRoleOptions: RoleToggleOption<keyof LearnerRoleSettingsDto>[] = [
    {
        key: "show_hero_block",
        label: "Показывать hero-блок",
        text: "Стартовый блок студента с расписанием и учебной сводкой.",
    },
    {
        key: "show_progress",
        label: "Показывать прогресс",
        text: "Личный прогресс по курсам, заданиям и целям.",
    },
    {
        key: "show_assignments",
        label: "Показывать задания",
        text: "Домашние работы, тесты и практические задания.",
    },
    {
        key: "show_schedule",
        label: "Показывать расписание",
        text: "Занятия, дедлайны и события календаря.",
    },
    {
        key: "show_achievements",
        label: "Показывать достижения",
        text: "Сертификаты, награды и учебные результаты.",
    },
    {
        key: "show_ai_hints",
        label: "AI-подсказки",
        text: "Рекомендации помощника по учебной траектории.",
    },
];

export const guardianRoleOptions: RoleToggleOption<keyof GuardianRoleSettingsDto>[] = [
    {
        key: "show_children_progress",
        label: "Показывать прогресс детей",
        text: "Сводка по успеваемости и активности связанных студентов.",
    },
    {
        key: "show_teacher_contacts",
        label: "Показывать контакты преподавателей",
        text: "Контактные данные преподавателей и кураторов.",
    },
    {
        key: "show_notifications",
        label: "Показывать уведомления",
        text: "Важные сообщения по детям, занятиям и успеваемости.",
    },
    {
        key: "show_schedule",
        label: "Показывать расписание",
        text: "Занятия, консультации и учебные события.",
    },
];

export const adminRoleOptions: RoleToggleOption<keyof AdminRoleSettingsDto>[] = [
    {
        key: "show_system_summary",
        label: "Показывать системную сводку",
        text: "Ключевые метрики платформы и состояния системы.",
    },
    {
        key: "show_moderation_panel",
        label: "Показывать модерацию",
        text: "Заявки, профили, материалы и другие объекты на проверке.",
    },
    {
        key: "show_audit_events",
        label: "Показывать аудит",
        text: "Последние системные и пользовательские события.",
    },
    {
        key: "show_support_requests",
        label: "Показывать обращения поддержки",
        text: "Заявки пользователей в техническую поддержку платформы.",
    },
];
