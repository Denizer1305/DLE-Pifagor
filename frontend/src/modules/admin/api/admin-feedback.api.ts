import { httpClient } from "@/services/api/http.client";
import type {
    AdminFeedbackFilters,
    AdminFeedbackListResponseDto,
    AdminFeedbackRequestDto,
    AdminFeedbackStatus,
} from "@/modules/admin/types/admin-feedback.types";

const ADMIN_FEEDBACK_URL = "/feedback/admin/requests/";

export async function fetchAdminFeedbackRequests(
    filters: AdminFeedbackFilters,
): Promise<AdminFeedbackListResponseDto> {
    const response = await httpClient.get<AdminFeedbackListResponseDto>(
        ADMIN_FEEDBACK_URL,
        { params: filters },
    );

    return response.data;
}

export async function patchAdminFeedbackStatus(
    requestId: number,
    status: AdminFeedbackStatus,
): Promise<AdminFeedbackRequestDto> {
    const response = await httpClient.patch<AdminFeedbackRequestDto>(
        `${ADMIN_FEEDBACK_URL}${requestId}/`,
        { status },
    );

    return response.data;
}
