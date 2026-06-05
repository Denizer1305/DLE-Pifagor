import type {
    CurrentProfileDto,
    ProfileContactItemModel,
    ProfileContactsCardModel,
    ProfileHeroModel,
    ProfileIdentityCardModel,
    ProfileRoleCode,
} from "@/modules/profile/types/profile.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

import fallbackAvatar from "@/assets/image/avatars/denizer1305.webp";

export function mapCurrentProfileToHero(dto: CurrentProfileDto): ProfileHeroModel {
    const avatarUrl = resolveBackendAssetUrl(dto.identity.avatar_url) || fallbackAvatar;

    return {
        topline: "Мой профиль",
        icon: "fas fa-user-shield",
        title: dto.identity.full_name || "Профиль пользователя",
        text: "Пространство, где собрана личная информация, активная роль, учебная или профессиональная нагрузка и цифровые каналы связи внутри платформы.",
        avatarUrl,
        avatarAlt: `Профиль пользователя ${dto.identity.full_name || ""}`.trim(),
        roleLabel: dto.active_role.label,
        subtitle: createProfileSubtitle(dto),
        badges: createProfileBadges(dto),
        stats: createProfileStats(dto),
    };
}

export function mapCurrentProfileToIdentityCard(
    dto: CurrentProfileDto,
): ProfileIdentityCardModel {
    return {
        title: "Основные сведения",
        text: "Персональная информация, которая используется внутри платформы для отображения профиля, идентификации пользователя и работы кабинета.",
        facts: [
            { label: "Полное имя", value: dto.identity.full_name || "Не указано" },
            { label: "Дата рождения", value: formatDate(dto.identity.birth_date) },
            { label: "Город", value: dto.identity.city || "Не указан" },
            { label: "Пол", value: formatGender(dto.identity.gender) },
        ],
    };
}

export function mapCurrentProfileToContactsCard(
    dto: CurrentProfileDto,
): ProfileContactsCardModel {
    return {
        title: "Цифровые каналы связи",
        text: "Здесь собраны основные способы связи с пользователем внутри и вне платформы.",
        contacts: createContactItems(dto),
        statuses: [
            {
                label: "Email",
                value: dto.contacts.is_email_verified ? "Подтверждён" : "Не подтверждён",
                isSuccess: dto.contacts.is_email_verified,
            },
            {
                label: "Телефон",
                value: dto.contacts.is_phone_verified ? "Подтверждён" : "Не подтверждён",
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
    if (isTeacherRole(dto.active_role.code)) {
        return [
            { icon: "fas fa-chalkboard-user", label: dto.active_role.label },
            { icon: "fas fa-building-columns", label: getString(dto.role_profile.organization) },
            { icon: "fas fa-briefcase", label: getString(dto.role_profile.department) },
        ].filter((badge) => badge.label && badge.label !== "Не указано");
    }

    if (dto.active_role.code === "learner") {
        return [
            { icon: "fas fa-user-graduate", label: dto.active_role.label },
            { icon: "fas fa-users", label: getString(dto.role_profile.group) },
            { icon: "fas fa-building-columns", label: getString(dto.role_profile.organization) },
        ].filter((badge) => badge.label && badge.label !== "Не указано");
    }

    return [{ icon: "fas fa-id-badge", label: dto.active_role.label }];
}

function createProfileStats(dto: CurrentProfileDto) {
    if (isTeacherRole(dto.active_role.code)) {
        return [
            { value: getString(dto.role_profile.experience_years), label: "лет стажа" },
            { value: dto.contacts.is_email_verified ? "Да" : "Нет", label: "email подтверждён" },
            { value: dto.display_settings.show_email ? "Вкл" : "Выкл", label: "публичный email" },
        ];
    }

    return [
        { value: dto.contacts.is_email_verified ? "Да" : "Нет", label: "email подтверждён" },
        { value: dto.display_settings.show_email ? "Вкл" : "Выкл", label: "email виден" },
        { value: dto.display_settings.show_phone ? "Вкл" : "Выкл", label: "телефон виден" },
    ];
}

function createProfileSubtitle(dto: CurrentProfileDto): string {
    if (isTeacherRole(dto.active_role.code)) {
        return getString(dto.role_profile.public_title) || dto.active_role.label;
    }

    return dto.active_role.code === "learner"
        ? getString(dto.role_profile.group) || dto.active_role.label
        : dto.active_role.label;
}

function isTeacherRole(roleCode: ProfileRoleCode): boolean {
    return ["teacher", "curator", "methodist", "organizer", "mentor"].includes(roleCode);
}

function getString(value: unknown): string {
    if (typeof value === "string" && value.trim()) {
        return value;
    }

    return typeof value === "number" ? String(value) : "Не указано";
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
    return value
        ? new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "long", year: "numeric" }).format(new Date(value))
        : "Не указана";
}
