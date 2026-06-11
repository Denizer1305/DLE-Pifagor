import { getCompositePrimaryActiveStatusBadge } from "../utils";
import type {
    OrganizationDetailsView,
    TeacherSubjectDto,
    TeacherSubjectListItemView,
} from "../types";
import {
    formatBoolean,
    formatDateTime,
    formatOptional,
} from "./organizations-common.mapper";

export function mapTeacherSubjectToListItem(
    dto: TeacherSubjectDto,
): TeacherSubjectListItemView {
    return {
        id: dto.id,
        teacherId: dto.teacher,
        teacherName: dto.teacher_full_name || `Преподаватель #${dto.teacher}`,
        teacherEmail: dto.teacher_email || "Email не указан",
        teacherPhone: dto.teacher_phone || "Телефон не указан",
        subjectTitle: dto.subject.short_name || dto.subject.name,
        subjectCode: dto.subject.code,
        isPrimary: dto.is_primary,
        isActive: dto.is_active,
        status: getCompositePrimaryActiveStatusBadge({
            isPrimary: dto.is_primary,
            isActive: dto.is_active,
        }),
        meta: [
            `Предмет: ${dto.subject.code}`,
            dto.is_primary ? "Основной предмет" : "Дополнительный предмет",
        ],
    };
}

export function mapTeacherSubjectsToListItems(
    items: TeacherSubjectDto[],
): TeacherSubjectListItemView[] {
    return items.map(mapTeacherSubjectToListItem);
}

export function mapTeacherSubjectToDetails(
    dto: TeacherSubjectDto,
): OrganizationDetailsView {
    return {
        title: dto.teacher_full_name || `Преподаватель #${dto.teacher}`,
        subtitle: dto.subject.name,
        eyebrow: "Предмет преподавателя",
        status: getCompositePrimaryActiveStatusBadge({
            isPrimary: dto.is_primary,
            isActive: dto.is_active,
        }),
        chips: [
            dto.subject.code,
            dto.is_primary ? "Основной" : "Дополнительный",
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
                label: "Предмет",
                value: dto.subject.name,
            },
            {
                label: "Код предмета",
                value: dto.subject.code,
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
