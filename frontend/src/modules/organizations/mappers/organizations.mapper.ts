import { getActiveStatusBadge } from "../utils";
import type {
    OrganizationDetailsView,
    OrganizationDto,
    OrganizationListItemView,
} from "../types";
import {
    formatBoolean,
    formatDateTime,
    formatOptional,
} from "./organizations-common.mapper";

export function mapOrganizationToListItem(
    dto: OrganizationDto,
): OrganizationListItemView {
    return {
        id: dto.id,
        title: dto.short_name || dto.name,
        subtitle: dto.name,
        code: dto.code,
        city: formatOptional(dto.city),
        email: formatOptional(dto.email),
        phone: formatOptional(dto.phone),
        website: formatOptional(dto.website),
        logoUrl: dto.logo,
        isActive: dto.is_active,
        isPublic: dto.is_public,
        isDefaultPublic: dto.is_default_public,
        status: getActiveStatusBadge(dto.is_active),
        meta: [
            `Код: ${dto.code}`,
            `Публичная: ${formatBoolean(dto.is_public)}`,
            `По умолчанию: ${formatBoolean(dto.is_default_public)}`,
        ],
    };
}

export function mapOrganizationsToListItems(
    items: OrganizationDto[],
): OrganizationListItemView[] {
    return items.map(mapOrganizationToListItem);
}

export function mapOrganizationToDetails(
    dto: OrganizationDto,
): OrganizationDetailsView {
    return {
        title: dto.short_name || dto.name,
        subtitle: dto.name,
        eyebrow: "Организация",
        status: getActiveStatusBadge(dto.is_active),
        chips: [
            dto.code,
            dto.city,
            dto.is_public ? "Публичная" : "Скрытая",
            dto.is_default_public ? "По умолчанию" : "",
        ].filter(Boolean),
        rows: [
            {
                label: "Полное название",
                value: dto.name,
            },
            {
                label: "Краткое название",
                value: formatOptional(dto.short_name),
            },
            {
                label: "Slug",
                value: dto.slug,
            },
            {
                label: "Код",
                value: dto.code,
            },
            {
                label: "Город",
                value: formatOptional(dto.city),
            },
            {
                label: "Адрес",
                value: formatOptional(dto.address),
            },
            {
                label: "Телефон",
                value: formatOptional(dto.phone),
            },
            {
                label: "Email",
                value: formatOptional(dto.email),
                href: dto.email ? `mailto:${dto.email}` : undefined,
            },
            {
                label: "Сайт",
                value: formatOptional(dto.website),
                href: dto.website || undefined,
            },
            {
                label: "Публичная",
                value: formatBoolean(dto.is_public),
            },
            {
                label: "Публичная по умолчанию",
                value: formatBoolean(dto.is_default_public),
            },
            {
                label: "Код преподавателя",
                value: dto.has_active_teacher_registration_code
                    ? "Активен"
                    : "Не настроен",
            },
            {
                label: "Код действует до",
                value: formatDateTime(dto.teacher_registration_code_expires_at),
            },
            {
                label: "Создана",
                value: formatDateTime(dto.created_at),
            },
            {
                label: "Обновлена",
                value: formatDateTime(dto.updated_at),
            },
        ],
    };
}