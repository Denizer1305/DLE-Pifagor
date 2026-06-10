import type {
    AdminFeedbackAttachment,
    AdminFeedbackAttachmentDto,
    AdminFeedbackList,
    AdminFeedbackListResponseDto,
    AdminFeedbackRequest,
    AdminFeedbackRequestDto,
} from "@/modules/admin/types/admin-feedback.types";

export function mapAdminFeedbackList(dto: AdminFeedbackListResponseDto): AdminFeedbackList {
    return {
        summary: {
            total: dto.summary.total,
            new: dto.summary.new,
            inProgress: dto.summary.in_progress,
            answered: dto.summary.answered,
            closed: dto.summary.closed,
        },
        items: dto.items.map(mapAdminFeedbackRequest),
    };
}

export function mapAdminFeedbackRequest(dto: AdminFeedbackRequestDto): AdminFeedbackRequest {
    return {
        id: dto.id,
        topic: dto.topic,
        status: dto.status,
        fullName: dto.full_name,
        email: dto.email,
        phone: dto.phone,
        organizationName: dto.organization_name,
        subject: dto.subject,
        message: dto.message,
        pageUrl: dto.page_url,
        attachmentCount: dto.attachment_count,
        attachments: (dto.attachments || []).map(mapAdminFeedbackAttachment),
        createdAt: dto.created_at,
    };
}

function mapAdminFeedbackAttachment(
    dto: AdminFeedbackAttachmentDto,
): AdminFeedbackAttachment {
    return {
        id: dto.id,
        name: dto.original_name,
        mimeType: dto.mime_type,
        size: dto.file_size,
        sizeLabel: formatFileSize(dto.file_size),
        kind: dto.kind,
        url: dto.url,
    };
}

function formatFileSize(size: number): string {
    if (size < 1024) {
        return `${size} Б`;
    }

    if (size < 1024 * 1024) {
        return `${(size / 1024).toFixed(1)} КБ`;
    }

    return `${(size / 1024 / 1024).toFixed(1)} МБ`;
}
