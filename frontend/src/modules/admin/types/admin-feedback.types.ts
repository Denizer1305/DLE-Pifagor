export type AdminFeedbackStatus =
    | "new"
    | "in_progress"
    | "answered"
    | "closed"
    | "spam";

export type AdminFeedbackTopic =
    | "question"
    | "partnership"
    | "organization_connection"
    | "technical_support"
    | "bug"
    | "other";

export interface AdminFeedbackRequestDto {
    id: number;
    topic: AdminFeedbackTopic;
    source: string;
    status: AdminFeedbackStatus;
    full_name: string;
    email: string;
    phone: string;
    organization_name: string;
    subject: string;
    message: string;
    page_url: string;
    attachment_count: number;
    attachments?: AdminFeedbackAttachmentDto[];
    created_at: string;
    updated_at: string;
}

export interface AdminFeedbackAttachmentDto {
    id: number;
    original_name: string;
    mime_type: string;
    file_size: number;
    kind: string;
    url: string;
}

export interface AdminFeedbackSummary {
    total: number;
    new: number;
    inProgress: number;
    answered: number;
    closed: number;
}

export interface AdminFeedbackListResponseDto {
    summary: {
        total: number;
        new: number;
        in_progress: number;
        answered: number;
        closed: number;
    };
    items: AdminFeedbackRequestDto[];
}

export interface AdminFeedbackRequest {
    id: number;
    topic: AdminFeedbackTopic;
    status: AdminFeedbackStatus;
    fullName: string;
    email: string;
    phone: string;
    organizationName: string;
    subject: string;
    message: string;
    pageUrl: string;
    attachmentCount: number;
    attachments: AdminFeedbackAttachment[];
    createdAt: string;
}

export interface AdminFeedbackAttachment {
    id: number;
    name: string;
    mimeType: string;
    size: number;
    sizeLabel: string;
    kind: string;
    url: string;
}

export interface AdminFeedbackFilters {
    status: AdminFeedbackStatus | "";
    topic: AdminFeedbackTopic | "";
    search: string;
}

export interface AdminFeedbackList {
    summary: AdminFeedbackSummary;
    items: AdminFeedbackRequest[];
}
