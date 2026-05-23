import type {
    DashboardCalendarContent,
    DashboardPageScaffoldModel,
    DashboardRole,
} from "@/components/dashboard/types/dashboard.types";
import { createProfileNavigation } from "@/modules/profile/data/profile-navigation.data";
import type {
    CurrentProfileDto,
    ProfileContactItemModel,
    ProfilePageModel,
    ProfileRoleCode,
    ProfileRoleSectionModel,
} from "@/modules/profile/types/profile.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

import logo from "@/assets/image/logo/logo.svg";
import anastasiaLogo from "@/assets/image/logo/Anastasia.svg";
import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

const dashboardTopbarLabels = {
    menu: "Открыть меню",
    calendar: "Открыть календарь",
    notifications: "Открыть уведомления",
    notes: "Открыть заметки",
    profile: "Открыть меню профиля",
    closePanel: "Закрыть панель",
};

export function mapCurrentProfileToPageModel(
    dto: CurrentProfileDto,
): ProfilePageModel {
    const scaffold = mapCurrentProfileToScaffoldModel(dto);
    const roleSection = mapCurrentProfileToRoleSection(dto);
    const avatarUrl = resolveBackendAssetUrl(dto.identity.avatar_url) || fallbackAvatar;

    return {
        scaffold,
        hero: {
            topline: "Мой профиль",
            icon: "fas fa-user-shield",
            title: dto.identity.full_name || "Профиль пользователя",
            text:
                "Пространство, где собрана личная информация, активная роль, учебная или профессиональная нагрузка и цифровые каналы связи внутри платформы.",
            avatarUrl,
            avatarAlt: `Профиль пользователя ${dto.identity.full_name || ""}`.trim(),
            roleLabel: dto.active_role.label,
            subtitle: createProfileSubtitle(dto),
            badges: createProfileBadges(dto),
            stats: createProfileStats(dto),
        },
        identityCard: {
            title: "Основные сведения",
            text:
                "Персональная информация, которая используется внутри платформы для отображения профиля, идентификации пользователя и работы кабинета.",
            facts: [
                {
                    label: "Полное имя",
                    value: dto.identity.full_name || "Не указано",
                },
                {
                    label: "Дата рождения",
                    value: formatDate(dto.identity.birth_date),
                },
                {
                    label: "Город",
                    value: dto.identity.city || "Не указан",
                },
                {
                    label: "Пол",
                    value: formatGender(dto.identity.gender),
                },
            ],
        },
        contactsCard: {
            title: "Цифровые каналы связи",
            text:
                "Здесь собраны основные способы связи с пользователем внутри и вне платформы.",
            contacts: createContactItems(dto),
            statuses: [
                {
                    label: "Email",
                    value: dto.contacts.is_email_verified
                        ? "Подтверждён"
                        : "Не подтверждён",
                    isSuccess: dto.contacts.is_email_verified,
                },
                {
                    label: "Телефон",
                    value: dto.contacts.is_phone_verified
                        ? "Подтверждён"
                        : "Не подтверждён",
                    isSuccess: dto.contacts.is_phone_verified,
                },
                {
                    label: "VK",
                    value: dto.contacts.vk_url ? "Подключен" : "Не подключен",
                    isSuccess: Boolean(dto.contacts.vk_url),
                },
                {
                    label: "MAX",
                    value: dto.contacts.max_url ? "Подключен" : "Не подключен",
                    isSuccess: Boolean(dto.contacts.max_url),
                },
            ],
        },
        roleSection,
    };
}

export function mapCurrentProfileToScaffoldModel(
    dto: CurrentProfileDto,
): DashboardPageScaffoldModel {
    const avatarUrl = resolveBackendAssetUrl(dto.identity.avatar_url) || fallbackAvatar;

    return {
        shell: createProfileShell(dto),
        calendarContent: createEmptyCalendarContent(),
        calendarDays: [],
        notifications: {
            title: "Уведомления",
            items: [],
            actionLabel: "Открыть уведомления",
            actionTo: {
                name: "notifications",
            },
        },
        notes: {
            title: "Заметки",
            createLabel: "Создать заметку",
            items: [],
            actionLabel: "Открыть все заметки",
            actionTo: {
                name: "notes",
            },
        },
        profilePanel: {
            user: {
                fullName: dto.identity.full_name || "Пользователь",
                roleLabel: dto.active_role.label,
                avatarUrl,
                avatarAlt: "Профиль пользователя",
            },
            title: "Профиль",
            subtitle: dto.active_role.label,
            actions: [
                {
                    label: "Мой профиль",
                    icon: "fas fa-user",
                    to: {
                        name: "profile",
                    },
                },
                {
                    label: "Редактировать профиль",
                    icon: "fas fa-pen-to-square",
                    to: {
                        name: "profile-edit",
                    },
                },
                {
                    label: "Достижения и награды",
                    icon: "fas fa-award",
                    to: {
                        name: "profile-achievements",
                    },
                },
                {
                    label: "Выйти",
                    icon: "fas fa-arrow-right-from-bracket",
                    action: "logout",
                },
            ],
        },
    };
}

function createProfileShell(dto: CurrentProfileDto) {
    const avatarUrl = resolveBackendAssetUrl(dto.identity.avatar_url) || fallbackAvatar;

    return {
        pageClass: `${mapRoleToPageClass(dto.active_role.code)} profile-page`,
        role: mapRoleToDashboardRole(dto.active_role.code),
        brand: {
            logo,
            title: "ПИФАГОР",
            subtitle: "Профиль пользователя",
        },
        profile: {
            fullName: dto.identity.full_name || "Пользователь",
            roleLabel: dto.active_role.label,
            avatarUrl,
            avatarAlt: "Профиль пользователя",
        },
        navigation: createProfileNavigation(dto.active_role.code),
        sidebarExtra: {
            variant: "ai" as const,
            title: "Анастасия",
            subtitle: "Помощник профиля",
            text:
                "Поможет оформить профиль, систематизировать достижения и аккуратно представить данные внутри платформы.",
            image: {
                src: anastasiaLogo,
                alt: "Анастасия",
            },
            action: {
                label: "Открыть Анастасию",
                icon: "fas fa-sparkles",
                to: {
                    name: "profile",
                },
            },
        },
        search: {
            placeholder: "Поиск по профилю, данным и документам...",
            ariaLabel: "Поиск по профилю",
        },
        topbarLabels: dashboardTopbarLabels,
        topbarUser: {
            fullName: dto.identity.full_name || "Пользователь",
            roleLabel: dto.active_role.label,
            avatarUrl,
            avatarAlt: "Профиль пользователя",
        },
    };
}

function mapCurrentProfileToRoleSection(dto: CurrentProfileDto): ProfileRoleSectionModel {
    const roleCode = dto.active_role.code;
    const roleProfile = dto.role_profile;

    if (isTeacherRole(roleCode)) {
        return {
            roleCode,
            title: "Профессиональный профиль преподавателя",
            text:
                "В этом разделе собрана информация, связанная с преподавательской ролью: специализация, нагрузка, дисциплины и методическая зона ответственности.",
            facts: [
                {
                    label: "Основная роль",
                    value: dto.active_role.label,
                },
                {
                    label: "Организация",
                    value: getString(roleProfile.organization),
                },
                {
                    label: "Подразделение",
                    value: getString(roleProfile.department),
                },
                {
                    label: "Должность",
                    value: getString(roleProfile.position),
                },
                {
                    label: "Публичный заголовок",
                    value: getString(roleProfile.public_title),
                },
                {
                    label: "Педагогический стаж",
                    value: formatExperience(roleProfile.experience_years),
                },
                {
                    label: "Статус",
                    value: getString(roleProfile.status),
                },
            ],
            tags: splitTags(getString(roleProfile.public_title)),
            groups: [],
            education: [
                {
                    title: "Образование",
                    text: getString(roleProfile.education),
                },
                {
                    title: "Профессиональные достижения",
                    text: getString(roleProfile.achievements),
                },
            ],
        };
    }

    if (roleCode === "learner") {
        return {
            roleCode,
            title: "Профиль студента",
            text:
                "Здесь собрана учебная информация студента: организация, группа, направление и текущий статус обучения.",
            facts: [
                {
                    label: "Основная роль",
                    value: dto.active_role.label,
                },
                {
                    label: "Организация",
                    value: getString(roleProfile.organization),
                },
                {
                    label: "Отделение",
                    value: getString(roleProfile.department),
                },
                {
                    label: "Группа",
                    value: getString(roleProfile.group),
                },
                {
                    label: "Куратор",
                    value: getString(roleProfile.curator),
                },
                {
                    label: "Год поступления",
                    value: getString(roleProfile.admission_year),
                },
                {
                    label: "Статус",
                    value: getString(roleProfile.status),
                },
            ],
            tags: [],
            groups: [],
            education: [],
        };
    }

    return {
        roleCode,
        title: "Роль пользователя",
        text:
            "Здесь отображается информация, связанная с активной ролью пользователя внутри платформы.",
        facts: [
            {
                label: "Активная роль",
                value: dto.active_role.label,
            },
        ],
        tags: [],
        groups: [],
        education: [],
    };
}

function createContactItems(dto: CurrentProfileDto): ProfileContactItemModel[] {
    return [
        {
            key: "email",
            label: "Электронная почта",
            value: dto.contacts.email || "Не указана",
            icon: "fas fa-envelope",
            href: dto.contacts.email ? `mailto:${dto.contacts.email}` : undefined,
            isVerified: dto.contacts.is_email_verified,
            isVisible: dto.contacts.show_email,
        },
        {
            key: "phone",
            label: "Телефон",
            value: dto.contacts.phone || "Не указан",
            icon: "fas fa-phone",
            href: dto.contacts.phone ? `tel:${dto.contacts.phone}` : undefined,
            isVerified: dto.contacts.is_phone_verified,
            isVisible: dto.contacts.show_phone,
        },
        {
            key: "vk",
            label: "VK",
            value: dto.contacts.vk_url || "Не подключен",
            icon: "fab fa-vk",
            href: dto.contacts.vk_url || undefined,
            isVerified: Boolean(dto.contacts.vk_url),
            isVisible: Boolean(dto.contacts.vk_url),
        },
        {
            key: "max",
            label: "MAX",
            value: dto.contacts.max_url || "Не подключен",
            icon: "fas fa-comment-dots",
            href: dto.contacts.max_url || undefined,
            isVerified: Boolean(dto.contacts.max_url),
            isVisible: Boolean(dto.contacts.max_url),
        },
    ];
}

function createProfileBadges(dto: CurrentProfileDto) {
    const roleCode = dto.active_role.code;

    if (isTeacherRole(roleCode)) {
        return [
            {
                icon: "fas fa-chalkboard-user",
                label: dto.active_role.label,
            },
            {
                icon: "fas fa-building-columns",
                label: getString(dto.role_profile.organization),
            },
            {
                icon: "fas fa-briefcase",
                label: getString(dto.role_profile.department),
            },
        ].filter((badge) => badge.label && badge.label !== "Не указано");
    }

    if (roleCode === "learner") {
        return [
            {
                icon: "fas fa-user-graduate",
                label: dto.active_role.label,
            },
            {
                icon: "fas fa-users",
                label: getString(dto.role_profile.group),
            },
            {
                icon: "fas fa-building-columns",
                label: getString(dto.role_profile.organization),
            },
        ].filter((badge) => badge.label && badge.label !== "Не указано");
    }

    return [
        {
            icon: "fas fa-id-badge",
            label: dto.active_role.label,
        },
    ];
}

function createProfileStats(dto: CurrentProfileDto) {
    const roleCode = dto.active_role.code;

    if (isTeacherRole(roleCode)) {
        return [
            {
                value: getString(dto.role_profile.experience_years),
                label: "лет стажа",
            },
            {
                value: dto.contacts.is_email_verified ? "Да" : "Нет",
                label: "email подтверждён",
            },
            {
                value: dto.display_settings.show_email ? "Вкл" : "Выкл",
                label: "публичный email",
            },
        ];
    }

    return [
        {
            value: dto.contacts.is_email_verified ? "Да" : "Нет",
            label: "email подтверждён",
        },
        {
            value: dto.display_settings.show_email ? "Вкл" : "Выкл",
            label: "email виден",
        },
        {
            value: dto.display_settings.show_phone ? "Вкл" : "Выкл",
            label: "телефон виден",
        },
    ];
}

function createProfileSubtitle(dto: CurrentProfileDto): string {
    if (isTeacherRole(dto.active_role.code)) {
        return getString(dto.role_profile.public_title) || dto.active_role.label;
    }

    if (dto.active_role.code === "learner") {
        return getString(dto.role_profile.group) || dto.active_role.label;
    }

    return dto.active_role.label;
}

function createEmptyCalendarContent(): DashboardCalendarContent {
    return {
        title: "Календарь",
        monthLabel: new Intl.DateTimeFormat("ru-RU", {
            month: "long",
            year: "numeric",
        }).format(new Date()),
        previousMonthLabel: "Предыдущий месяц",
        nextMonthLabel: "Следующий месяц",
        weekdays: [
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб",
            "Вс",
        ],
    };
}

function mapRoleToDashboardRole(roleCode: ProfileRoleCode): DashboardRole {
    if (isTeacherRole(roleCode)) {
        return "teacher";
    }

    if (roleCode === "learner") {
        return "student";
    }

    if (roleCode === "guardian") {
        return "parent";
    }

    return "admin";
}

function mapRoleToPageClass(roleCode: ProfileRoleCode): string {
    if (isTeacherRole(roleCode)) {
        return "teacher-dashboard-page";
    }

    if (roleCode === "learner") {
        return "student-dashboard-page";
    }

    if (roleCode === "guardian") {
        return "parent-dashboard-page";
    }

    return "admin-dashboard-page";
}

function isTeacherRole(roleCode: ProfileRoleCode): boolean {
    return [
        "teacher",
        "curator",
        "methodist",
        "organizer",
        "mentor",
    ].includes(roleCode);
}

function getString(value: unknown): string {
    if (typeof value === "string" && value.trim()) {
        return value;
    }

    if (typeof value === "number") {
        return String(value);
    }

    return "Не указано";
}

function splitTags(value: string): string[] {
    if (!value || value === "Не указано") {
        return [];
    }

    return value
        .split(/[·,;/]/)
        .map((item) => item.trim())
        .filter(Boolean);
}

function formatExperience(value: unknown): string {
    if (typeof value === "number") {
        return `${value} лет`;
    }

    return getString(value);
}

function formatGender(value: string): string {
    const labels: Record<string, string> = {
        male: "Мужской",
        female: "Женский",
        not_specified: "Не указан",
        unknown: "Не указан",
    };

    return labels[value] || "Не указан";
}

function formatDate(value: string | null): string {
    if (!value) {
        return "Не указана";
    }

    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
    }).format(new Date(value));
}
