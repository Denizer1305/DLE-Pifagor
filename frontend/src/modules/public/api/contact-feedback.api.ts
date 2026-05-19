import { httpClient } from "@/services/api/http.client";
import type {
    ContactFeedbackPayload,
    ContactFeedbackResponse,
} from "@/modules/public/types/contact.types";

const CONTACT_FEEDBACK_URL = "/feedback/contact/";

function appendIfFilled(
    formData: FormData,
    key: string,
    value: string | undefined,
): void {
    const normalizedValue = value?.trim();

    if (normalizedValue) {
        formData.append(key, normalizedValue);
    }
}

export async function sendContactFeedback(
    payload: ContactFeedbackPayload,
): Promise<ContactFeedbackResponse> {
    const formData = new FormData();

    formData.append("topic", payload.topic);
    formData.append("full_name", payload.fullName.trim());
    formData.append("email", payload.email.trim());
    formData.append("message", payload.message.trim());
    formData.append(
        "is_personal_data_consent",
        payload.isPersonalDataConsent ? "true" : "false",
    );

    appendIfFilled(formData, "phone", payload.phone);
    appendIfFilled(formData, "organization_name", payload.organizationName);
    appendIfFilled(formData, "subject", payload.subject);
    appendIfFilled(formData, "page_url", payload.pageUrl);
    appendIfFilled(formData, "frontend_route", payload.frontendRoute);

    payload.attachments?.forEach((file) => {
        formData.append("attachments", file, file.name);
    });

    const response = await httpClient.post<ContactFeedbackResponse>(
        CONTACT_FEEDBACK_URL,
        formData,
    );

    return response.data;
}
