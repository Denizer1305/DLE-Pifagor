import { JOIN_REQUEST_TYPE_OPTIONS } from "../data";
import {
    getJoinRequestStatusBadge,
    isPendingJoinRequest,
} from "../utils";
import type {
    JoinRequestDto,
    JoinRequestListItemView,
    JoinRequestTypeApi,
    OrganizationDetailsView,
} from "../types";
import {
    formatDateTime,
    formatOptional,
    getUserContacts,
    getUserDisplayName,
} from "./organizations-common.mapper";

export function mapJoinRequestToListItem(
    dto: JoinRequestDto,
): JoinRequestListItemView {
    return {
        id: dto.id,
        type: dto.request_type,
        typeLabel: getJoinRequestTypeLabel(dto.request_type),
        statusCode: dto.status,
        status: getJoinRequestStatusBadge(dto.status),
        userName: getUserDisplayName(dto.user),
        userContacts: getUserContacts(dto.user),
        targetTitle: getJoinRequestTargetTitle(dto),
        message: dto.message || "Сообщение не указано",
        reviewComment: dto.review_comment || "",
        createdAtLabel: formatDateTime(dto.created_at),
        reviewedAtLabel: formatDateTime(dto.reviewed_at),
        canReview: isPendingJoinRequest(dto.status),
        meta: [
            getJoinRequestTypeLabel(dto.request_type),
            getJoinRequestTargetTitle(dto),
            `Создана: ${formatDateTime(dto.created_at)}`,
        ],
    };
}

export function mapJoinRequestsToListItems(
    items: JoinRequestDto[],
): JoinRequestListItemView[] {
    return items.map(mapJoinRequestToListItem);
}

export function mapJoinRequestToDetails(
    dto: JoinRequestDto,
): OrganizationDetailsView {
    return {
        title: getUserDisplayName(dto.user),
        subtitle: getJoinRequestTargetTitle(dto),
        eyebrow: getJoinRequestTypeLabel(dto.request_type),
        status: getJoinRequestStatusBadge(dto.status),
        chips: [
            getJoinRequestTypeLabel(dto.request_type),
            dto.organization?.short_name || dto.organization?.name || "",
            dto.group?.name || "",
        ].filter(Boolean),
        rows: [
            {
                label: "Пользователь",
                value: getUserDisplayName(dto.user),
            },
            {
                label: "Контакты",
                value: getUserContacts(dto.user),
            },
            {
                label: "Тип заявки",
                value: getJoinRequestTypeLabel(dto.request_type),
            },
            {
                label: "Организация",
                value: dto.organization?.name || "Не указана",
            },
            {
                label: "Отделение",
                value: dto.department?.name || "Не указано",
            },
            {
                label: "Группа",
                value: dto.group?.name || "Не указана",
            },
            {
                label: "Целевой пользователь",
                value: dto.target_user
                    ? getUserDisplayName(dto.target_user)
                    : "Не указан",
            },
            {
                label: "Сообщение",
                value: formatOptional(dto.message),
            },
            {
                label: "Комментарий проверки",
                value: formatOptional(dto.review_comment),
            },
            {
                label: "Проверил",
                value: dto.reviewed_by
                    ? getUserDisplayName(dto.reviewed_by)
                    : "Не проверено",
            },
            {
                label: "Создана",
                value: formatDateTime(dto.created_at),
            },
            {
                label: "Рассмотрена",
                value: formatDateTime(dto.reviewed_at),
            },
            {
                label: "Истекает",
                value: formatDateTime(dto.expires_at),
            },
        ],
    };
}

export function getJoinRequestTypeLabel(value: JoinRequestTypeApi): string {
    return JOIN_REQUEST_TYPE_OPTIONS.find((item) => item.value === value)
        ?.label ?? value;
}

export function getJoinRequestTargetTitle(dto: JoinRequestDto): string {
    if (dto.request_type === "teacher_to_organization") {
        return dto.organization?.short_name || dto.organization?.name || "Организация не указана";
    }

    if (dto.request_type === "learner_to_group") {
        return [
            dto.group?.name,
            dto.department?.short_name || dto.department?.name,
        ]
            .filter(Boolean)
            .join(" · ") || "Группа не указана";
    }

    if (dto.request_type === "guardian_to_learner") {
        return dto.target_user
            ? getUserDisplayName(dto.target_user)
            : "Учащийся не указан";
    }

    return "Цель заявки не указана";
}