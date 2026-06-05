import {
    fetchAdminFeedbackRequests,
    patchAdminFeedbackStatus,
} from "@/modules/admin/api/admin-feedback.api";
import {
    mapAdminFeedbackList,
    mapAdminFeedbackRequest,
} from "@/modules/admin/mappers/admin-feedback.mapper";
import type {
    AdminFeedbackFilters,
    AdminFeedbackList,
    AdminFeedbackRequest,
    AdminFeedbackStatus,
} from "@/modules/admin/types/admin-feedback.types";

export async function getAdminFeedbackRequests(
    filters: AdminFeedbackFilters,
): Promise<AdminFeedbackList> {
    return mapAdminFeedbackList(await fetchAdminFeedbackRequests(filters));
}

export async function updateAdminFeedbackStatus(
    requestId: number,
    status: AdminFeedbackStatus,
): Promise<AdminFeedbackRequest> {
    return mapAdminFeedbackRequest(await patchAdminFeedbackStatus(requestId, status));
}
