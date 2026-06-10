import { getActiveStatusBadge } from "../utils";
import type {
    OrganizationDetailsView,
    SubjectDto,
    SubjectListItemView,
} from "../types";
import {
    formatBoolean,
    formatDateTime,
    formatOptional,
} from "./organizations-common.mapper";

export function mapSubjectToListItem(dto: SubjectDto): SubjectListItemView {
    return {
        id: dto.id,
        title: dto.short_name || dto.name,
        subtitle: dto.name,
        code: dto.code,
        isActive: dto.is_active,
        status: getActiveStatusBadge(dto.is_active),
        meta: [
            `Код: ${dto.code}`,
            dto.description ? dto.description : "Описание не указано",
        ],
    };
}

export function mapSubjectsToListItems(
    items: SubjectDto[],
): SubjectListItemView[] {
    return items.map(mapSubjectToListItem);
}

export function mapSubjectToDetails(
    dto: SubjectDto,
): OrganizationDetailsView {
    return {
        title: dto.short_name || dto.name,
        subtitle: dto.name,
        eyebrow: "Учебный предмет",
        status: getActiveStatusBadge(dto.is_active),
        chips: [dto.code].filter(Boolean),
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
                label: "Описание",
                value: formatOptional(dto.description),
            },
            {
                label: "Активен",
                value: formatBoolean(dto.is_active),
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