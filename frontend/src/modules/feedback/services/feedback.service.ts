import { postFeedbackRequest } from "@/modules/feedback/api/feedback.api";
import type {
    ContactFeedbackPayload,
    ContactFeedbackResponse,
} from "@/modules/public/types/contact.types";

export function createFeedbackRequest(
    payload: ContactFeedbackPayload,
): Promise<ContactFeedbackResponse> {
    return postFeedbackRequest(payload);
}
