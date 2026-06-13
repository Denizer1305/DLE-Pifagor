import { getStudyGroupStatusBadge } from "../utils";
import type {
    OrganizationDetailsView,
    StudyGroupDto,
    StudyGroupListItemView,
} from "../types";
import {
    formatBoolean,
    formatDateTime,
    formatOptional,
    formatYear,
} from "./organizations-common.mapper";

export function mapStudyGroupToListItem(
    dto: StudyGroupDto,
): StudyGroupListItemView {
    return {
        id: dto.id,
        title: dto.name,
        subtitle: dto.description || dto.code,
        code: dto.code,
        organizationTitle: dto.organization.short_name || dto.organization.name,
        departmentTitle: dto.department?.short_name || dto.department?.name || "Без отделения",
        admissionYear: formatYear(dto.admission_year),
        graduationYear: formatYear(dto.graduation_year),
        courseNumber: dto.course_number ? `${dto.course_number} курс` : "—",
        statusCode: dto.status,
        status: getStudyGroupStatusBadge(dto.status),
        isActive: dto.is_active,
        isArchived: dto.is_archived,
        meta: [
            `Код: ${dto.code}`,
            `Поступление: ${formatYear(dto.admission_year)}`,
            `Выпуск: ${formatYear(dto.graduation_year)}`,
        ],
    };
}

export function mapStudyGroupsToListItems(
    items: StudyGroupDto[],
): StudyGroupListItemView[] {
    return items.map(mapStudyGroupToListItem);
}

export function mapStudyGroupToDetails(
    dto: StudyGroupDto,
): OrganizationDetailsView {
    return {
        title: dto.name,
        subtitle: dto.department?.name || dto.organization.name,
        eyebrow: "Учебная группа",
        status: getStudyGroupStatusBadge(dto.status),
        chips: [
            dto.code,
            dto.course_number ? `${dto.course_number} курс` : "",
            dto.is_archived ? "Архив" : "Активная структура",
        ].filter(Boolean),
        rows: [
            {
                label: "Название",
                value: dto.name,
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
                label: "Отделение",
                value: dto.department?.name || "Без отделения",
            },
            {
                label: "Описание",
                value: formatOptional(dto.description),
            },
            {
                label: "Год поступления",
                value: formatYear(dto.admission_year),
            },
            {
                label: "Год выпуска",
                value: formatYear(dto.graduation_year),
            },
            {
                label: "Курс",
                value: dto.course_number ? `${dto.course_number}` : "—",
            },
            {
                label: "Активна",
                value: formatBoolean(dto.is_active),
            },
            {
                label: "В архиве",
                value: formatBoolean(dto.is_archived),
            },
            {
                label: "Код вступления",
                value: dto.has_active_join_code ? "Активен" : "Не настроен",
            },
            {
                label: "Код действует до",
                value: formatDateTime(dto.join_code_expires_at),
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
