import {
    ACTIVE_STATUS_OPTION,
    INACTIVE_STATUS_OPTION,
    JOIN_REQUEST_STATUS_OPTIONS,
    PRIMARY_STATUS_OPTION,
    SECONDARY_STATUS_OPTION,
    STUDY_GROUP_STATUS_OPTIONS,
} from "../data";
import type {
    JoinRequestStatusApi,
    StatusBadgeView,
    StudyGroupStatusApi,
} from "../types";

function createStatusBadge(
    label: string,
    className: string,
    tone: StatusBadgeView["tone"],
): StatusBadgeView {
    return {
        label,
        className,
        tone,
    };
}

export function getActiveStatusBadge(isActive: boolean): StatusBadgeView {
    const option = isActive ? ACTIVE_STATUS_OPTION : INACTIVE_STATUS_OPTION;

    return createStatusBadge(option.label, option.className, option.tone);
}

export function getPrimaryStatusBadge(isPrimary: boolean): StatusBadgeView {
    const option = isPrimary ? PRIMARY_STATUS_OPTION : SECONDARY_STATUS_OPTION;

    return createStatusBadge(option.label, option.className, option.tone);
}

export function getStudyGroupStatusBadge(
    status: StudyGroupStatusApi,
): StatusBadgeView {
    const option = STUDY_GROUP_STATUS_OPTIONS.find(
        (item) => item.value === status,
    );

    if (!option) {
        return getActiveStatusBadge(false);
    }

    return createStatusBadge(option.label, option.className, option.tone);
}

export function getJoinRequestStatusBadge(
    status: JoinRequestStatusApi,
): StatusBadgeView {
    const option = JOIN_REQUEST_STATUS_OPTIONS.find(
        (item) => item.value === status,
    );

    if (!option) {
        return getActiveStatusBadge(false);
    }

    return createStatusBadge(option.label, option.className, option.tone);
}

type CompositePrimaryActiveStatusParams = {
    isPrimary: boolean;
    isActive: boolean;
};

export function getCompositePrimaryActiveStatusBadge(
    params: CompositePrimaryActiveStatusParams,
): StatusBadgeView {
    const { isPrimary, isActive } = params;

    if (!isActive) {
        return getActiveStatusBadge(false);
    }

    return getPrimaryStatusBadge(isPrimary);
}

export function isPendingJoinRequest(status: JoinRequestStatusApi): boolean {
    return status === "pending";
}

export function isApprovedJoinRequest(status: JoinRequestStatusApi): boolean {
    return status === "approved";
}

export function isRejectedJoinRequest(status: JoinRequestStatusApi): boolean {
    return status === "rejected";
}
