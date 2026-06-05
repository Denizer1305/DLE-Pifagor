import type {
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
} from "@/modules/public/types/contact.types";

export function createInitialContactFeedbackForm(): ContactFeedbackFormState {
    return {
        topic: "question",
        fullName: "",
        email: "",
        phone: "",
        organizationName: "",
        subject: "",
        message: "",
        isPersonalDataConsent: false,
        attachments: [],
    };
}

export function createInitialContactFeedbackErrors(): ContactFeedbackFormErrors {
    return {
        topic: "",
        fullName: "",
        email: "",
        phone: "",
        organizationName: "",
        subject: "",
        message: "",
        isPersonalDataConsent: "",
        attachments: "",
        common: "",
    };
}

export function normalizeContactFeedbackText(value: string): string {
    return value.trim().replace(/\s+/g, " ");
}
