import { TEACHER_EMPLOYMENT_TYPE_OPTIONS } from "../data";
import { getCompositePrimaryActiveStatusBadge } from "../utils";
import type {
    OrganizationDetailsView,
    TeacherEmploymentTypeApi,
    TeacherOrganizationDto,
    TeacherOrganizationListItemView,
} from "../types";
import {
    formatBoolean,
    formatDate,
    formatDateTime,
    formatOptional,
} from "./organizations-common.mapper";

export function mapTeacherOrganizationToListItem(
    dto: TeacherOrganizationDto,
): TeacherOrganizationListItemView {
    return {
        id: dto.id,
        teacherId: dto.teacher,
        teacherName: dto.teacher_full_name || `Преподаватель #${dto.teacher}`,
        teacherEmail: dto.teacher_email || "Email не указан",
        teacherPhone: dto.teacher_phone || "Телефон не указан",
        organizationTitle: dto.organization.short_name || dto.organization.name,
        position: formatOptional(dto.position),
        employmentTypeLabel: getEmploymentTypeLabel(dto.employment_type),
        isPrimary: dto.is_primary,
        isActive: dto.is_active,
        status: getCompositePrimaryActiveStatusBadge({
            isPrimary: dto.is_primary,
            isActive: dto.is_active,
        }),
        meta: [
            getEmploymentTypeLabel(dto.employment_type),
            dto.is_primary ? "Основная организация" : "Дополнительная организация",
        ],
    };
}

export function mapTeacherOrganizationsToListItems(
    items: TeacherOrganizationDto[],
): TeacherOrganizationListItemView[] {
    return items.map(mapTeacherOrganizationToListItem);
}

export function mapTeacherOrganizationToDetails(
    dto: TeacherOrganizationDto,
): OrganizationDetailsView {
    return {
        title: dto.teacher_full_name || `Преподаватель #${dto.teacher}`,
        subtitle: dto.organization.name,
        eyebrow: "Преподаватель организации",
        status: getCompositePrimaryActiveStatusBadge({
            isPrimary: dto.is_primary,
            isActive: dto.is_active,
        }),
        chips: [
            getEmploymentTypeLabel(dto.employment_type),
            dto.is_primary ? "Основная" : "Дополнительная",
        ],
        rows: [
            {
                label: "Преподаватель",
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
                label: "Организация",
                value: dto.organization.name,
            },
            {
                label: "Должность",
                value: formatOptional(dto.position),
            },
            {
                label: "Тип занятости",
                value: getEmploymentTypeLabel(dto.employment_type),
            },
            {
                label: "Основная",
                value: formatBoolean(dto.is_primary),
            },
            {
                label: "Активна",
                value: formatBoolean(dto.is_active),
            },
            {
                label: "Начало работы",
                value: formatDate(dto.starts_at),
            },
            {
                label: "Окончание работы",
                value: formatDate(dto.ends_at),
            },
            {
                label: "Заметки",
                value: formatOptional(dto.notes),
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

export function getEmploymentTypeLabel(
    value: TeacherEmploymentTypeApi,
): string {
    return TEACHER_EMPLOYMENT_TYPE_OPTIONS.find((item) => item.value === value)
        ?.label ?? value;
}