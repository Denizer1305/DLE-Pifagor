import { sendContactFeedback } from "@/modules/public/api/contact-feedback.api";
import type {
    ContactFeedbackPayload,
    ContactFeedbackResponse,
} from "@/modules/public/types/contact.types";

export function postFeedbackRequest(
    payload: ContactFeedbackPayload,
): Promise<ContactFeedbackResponse> {
    return sendContactFeedback(payload);
}
