import { getCompositePrimaryActiveStatusBadge } from "../utils";
import type {
    GroupCuratorDto,
    GroupCuratorListItemView,
    OrganizationDetailsView,
} from "../types";
import {
    formatBoolean,
    formatDate,
    formatDateTime,
    formatOptional,
} from "./organizations-common.mapper";

export function mapGroupCuratorToListItem(
    dto: GroupCuratorDto,
): GroupCuratorListItemView {
    return {
        id: dto.id,
        teacherId: dto.teacher,
        teacherName: dto.teacher_full_name || `Преподаватель #${dto.teacher}`,
        teacherEmail: dto.teacher_email || "Email не указан",
        teacherPhone: dto.teacher_phone || "Телефон не указан",
        groupTitle: dto.group.name,
        isPrimary: dto.is_primary,
        isActive: dto.is_active,
        status: getCompositePrimaryActiveStatusBadge({
            isPrimary: dto.is_primary,
            isActive: dto.is_active,
        }),
        meta: [
            `Группа: ${dto.group.code}`,
            dto.is_primary ? "Основной куратор" : "Дополнительный куратор",
        ],
    };
}

export function mapGroupCuratorsToListItems(
    items: GroupCuratorDto[],
): GroupCuratorListItemView[] {
    return items.map(mapGroupCuratorToListItem);
}

export function mapGroupCuratorToDetails(
    dto: GroupCuratorDto,
): OrganizationDetailsView {
    return {
        title: dto.teacher_full_name || `Преподаватель #${dto.teacher}`,
        subtitle: dto.group.name,
        eyebrow: "Куратор группы",
        status: getCompositePrimaryActiveStatusBadge({
            isPrimary: dto.is_primary,
            isActive: dto.is_active,
        }),
        chips: [
            dto.group.code,
            dto.is_primary ? "Основной" : "Дополнительный",
        ],
        rows: [
            {
                label: "Куратор",
                value: dto.teacher_full_name || `#${dto.teacher}`,
            },
            {
                label: "Email",
                value: formatOptional(dto.teacher_email),
                href: dto.teacher_email ? `mailto:${dto.teacher_email}` : undefined,
            },
            {
                label: "Телефон",
                value: formatOptional(dto.teacher_phone),
            },
            {
                label: "Группа",
                value: dto.group.name,
            },
            {
                label: "Код группы",
                value: dto.group.code,
            },
            {
                label: "Основной",
                value: formatBoolean(dto.is_primary),
            },
            {
                label: "Активен",
                value: formatBoolean(dto.is_active),
            },
            {
                label: "Начало",
                value: formatDate(dto.starts_at),
            },
            {
                label: "Окончание",
                value: formatDate(dto.ends_at),
            },
            {
                label: "Заметки",
                value: formatOptional(dto.notes),
            },
            {
                label: "Создан",
                value: formatDateTime(dto.created_at),
            },
            {
                label: "Обновлён",
                value: formatDateTime(dto.updated_at),
            },
        ],
    };
}