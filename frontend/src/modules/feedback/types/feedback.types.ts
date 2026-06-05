import type {
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
    ContactFeedbackResponse,
    ContactFeedbackTopic,
} from "@/modules/public/types/contact.types";

export type FeedbackTopic = ContactFeedbackTopic;

export type FeedbackFormState = ContactFeedbackFormState;

export type FeedbackFormErrors = ContactFeedbackFormErrors;

export type FeedbackCreateResponse = ContactFeedbackResponse;

export interface FeedbackPageContent {
    loadingText: string;
    errorTitle: string;
    retryLabel: string;
    retryIcon: string;
    hero: {
        badge: string;
        title: string;
        text: string;
    };
    info: {
        title: string;
        text: string;
        items: {
            icon: string;
            title: string;
            text: string;
        }[];
    };
    form: {
        title: string;
        text: string;
        topicLabel: string;
        subjectLabel: string;
        subjectPlaceholder: string;
        messageLabel: string;
        messagePlaceholder: string;
        filesLabel: string;
        filesHint: string;
        filesButtonLabel: string;
        removeFileLabel: string;
        nameLabel: string;
        emailLabel: string;
        phoneLabel: string;
        organizationLabel: string;
        consentLabel: string;
        submitLabel: string;
        submittingLabel: string;
        successTitle: string;
        successText: string;
        resetLabel: string;
    };
    topics: {
        value: FeedbackTopic;
        label: string;
    }[];
}
