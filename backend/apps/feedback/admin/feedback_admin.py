from __future__ import annotations

from apps.feedback.models import FeedbackAttachment, FeedbackRequest
from django.contrib import admin


class FeedbackAttachmentInline(admin.TabularInline):
    model = FeedbackAttachment
    extra = 0
    readonly_fields = (
        "original_name",
        "mime_type",
        "file_size",
        "kind",
        "created_at",
    )


@admin.register(FeedbackRequest)
class FeedbackRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "topic",
        "source",
        "status",
        "admin_notification_sent",
        "created_at",
    )
    list_filter = (
        "topic",
        "source",
        "status",
        "admin_notification_sent",
        "created_at",
    )
    search_fields = (
        "full_name",
        "email",
        "phone",
        "organization_name",
        "subject",
        "message",
    )
    readonly_fields = (
        "user",
        "topic",
        "source",
        "full_name",
        "email",
        "phone",
        "organization_name",
        "subject",
        "message",
        "is_personal_data_consent",
        "page_url",
        "frontend_route",
        "error_code",
        "error_details",
        "ip_address",
        "user_agent",
        "admin_notification_sent",
        "admin_notification_error",
        "created_at",
        "updated_at",
    )
    inlines = (FeedbackAttachmentInline,)
    fieldsets = (
        (
            "Обращение",
            {
                "fields": (
                    "status",
                    "topic",
                    "source",
                    "subject",
                    "message",
                )
            },
        ),
        (
            "Контактные данные",
            {
                "fields": (
                    "user",
                    "full_name",
                    "email",
                    "phone",
                    "organization_name",
                    "is_personal_data_consent",
                )
            },
        ),
        (
            "Техническая информация",
            {
                "fields": (
                    "page_url",
                    "frontend_route",
                    "error_code",
                    "error_details",
                    "ip_address",
                    "user_agent",
                )
            },
        ),
        (
            "Email-уведомление",
            {
                "fields": (
                    "admin_notification_sent",
                    "admin_notification_error",
                )
            },
        ),
        (
            "Служебные даты",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(FeedbackAttachment)
class FeedbackAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "feedback_request",
        "original_name",
        "kind",
        "file_size",
        "created_at",
    )
    list_filter = (
        "kind",
        "created_at",
    )
    search_fields = (
        "original_name",
        "feedback_request__full_name",
        "feedback_request__email",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
