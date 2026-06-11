import { getActiveStatusBadge } from "../utils";
import type {
    DepartmentDto,
    DepartmentListItemView,
    OrganizationDetailsView,
} from "../types";
import {
    formatBoolean,
    formatDateTime,
    formatOptional,
} from "./organizations-common.mapper";

export function mapDepartmentToListItem(
    dto: DepartmentDto,
): DepartmentListItemView {
    return {
        id: dto.id,
        title: dto.short_name || dto.name,
        subtitle: dto.name,
        code: dto.code,
        organizationTitle: dto.organization.short_name || dto.organization.name,
        isActive: dto.is_active,
        status: getActiveStatusBadge(dto.is_active),
        meta: [
            `Код: ${dto.code}`,
            `Организация: ${dto.organization.short_name || dto.organization.name}`,
        ],
    };
}

export function mapDepartmentsToListItems(
    items: DepartmentDto[],
): DepartmentListItemView[] {
    return items.map(mapDepartmentToListItem);
}

export function mapDepartmentToDetails(
    dto: DepartmentDto,
): OrganizationDetailsView {
    return {
        title: dto.short_name || dto.name,
        subtitle: dto.organization.short_name || dto.organization.name,
        eyebrow: "Отделение",
        status: getActiveStatusBadge(dto.is_active),
        chips: [
            dto.code,
            dto.organization.short_name || dto.organization.name,
        ].filter(Boolean),
        rows: [
            {
                label: "Название",
                value: dto.name,
            },
            {
                label: "Краткое название",
                value: formatOptional(dto.short_name),
            },
            {
                label: "Код",
                value: dto.code,
            },
            {
                label: "Организация",
                value: dto.organization.name,
            },
            {
                label: "Активно",
                value: formatBoolean(dto.is_active),
            },
            {
                label: "Создано",
                value: formatDateTime(dto.created_at),
            },
            {
                label: "Обновлено",
                value: formatDateTime(dto.updated_at),
            },
        ],
    };
}
