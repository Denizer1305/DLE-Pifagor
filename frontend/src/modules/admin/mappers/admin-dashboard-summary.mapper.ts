import { mapAdminCalendar } from "@/modules/admin/mappers/admin-dashboard-calendar.mapper";
import type {
    AdminDashboardAuditActor,
    AdminDashboardAuditActorDto,
    AdminDashboardAuditEvent,
    AdminDashboardAuditEventDto,
    AdminDashboardFeedbackRequest,
    AdminDashboardFeedbackRequestDto,
    AdminDashboardJoinRequest,
    AdminDashboardJoinRequestDto,
    AdminDashboardProfile,
    AdminDashboardProfileDto,
    AdminDashboardQuickAction,
    AdminDashboardQuickActionDto,
    AdminDashboardStat,
    AdminDashboardStatDto,
    AdminDashboardSummary,
    AdminDashboardSummaryDto,
    AdminDashboardSystemCheck,
    AdminDashboardSystemCheckDto,
    AdminDashboardSystemHealth,
    AdminDashboardSystemHealthDto,
    AdminDashboardUserShort,
    AdminDashboardUserShortDto,
} from "@/modules/admin/types/admin-dashboard.types";
import { resolveBackendAssetUrl } from "@/utils/backend-asset-url.utils";

export function mapAdminDashboardSummary(
    dto: AdminDashboardSummaryDto,
): AdminDashboardSummary {
    return {
        profile: mapProfile(dto.profile),
        stats: dto.stats.map(mapStat),
        calendar: mapAdminCalendar(dto.calendar),
        recentUsers: dto.recent_users.map(mapUserShort),
        joinRequests: dto.join_requests.map(mapJoinRequest),
        feedbackRequests: dto.feedback_requests.map(mapFeedbackRequest),
        auditEvents: dto.audit_events.map(mapAuditEvent),
        systemHealth: mapSystemHealth(dto.system_health),
        quickActions: dto.quick_actions.map(mapQuickAction),
    };
}

function mapProfile(dto: AdminDashboardProfileDto): AdminDashboardProfile {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        avatarUrl: resolveBackendAssetUrl(dto.avatar_url),
        roleLabel: dto.role_label,
    };
}

function mapStat(dto: AdminDashboardStatDto): AdminDashboardStat {
    return {
        key: dto.key,
        label: dto.label,
        value: dto.value,
        caption: dto.caption,
        icon: dto.icon,
        tone: dto.tone,
    };
}

function mapUserShort(dto: AdminDashboardUserShortDto): AdminDashboardUserShort {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        status: dto.status,
        createdAt: dto.created_at,
    };
}

function mapJoinRequest(dto: AdminDashboardJoinRequestDto): AdminDashboardJoinRequest {
    return {
        id: dto.id,
        requestType: dto.request_type,
        status: dto.status,
        user: mapUserShort(dto.user),
        organization: dto.organization,
        department: dto.department,
        group: dto.group,
        message: dto.message,
        createdAt: dto.created_at,
    };
}

function mapFeedbackRequest(dto: AdminDashboardFeedbackRequestDto): AdminDashboardFeedbackRequest {
    return {
        id: dto.id,
        fullName: dto.full_name,
        email: dto.email,
        topic: dto.topic,
        status: dto.status,
        message: dto.message,
        createdAt: dto.created_at,
    };
}

function mapAuditActor(
    dto: AdminDashboardAuditActorDto | null,
): AdminDashboardAuditActor | null {
    return dto
        ? { id: dto.id, fullName: dto.full_name, email: dto.email }
        : null;
}

function mapAuditEvent(dto: AdminDashboardAuditEventDto): AdminDashboardAuditEvent {
    return {
        id: dto.id,
        action: dto.action,
        message: dto.message,
        actor: mapAuditActor(dto.actor),
        targetUser: mapAuditActor(dto.target_user),
        createdAt: dto.created_at,
    };
}

function mapSystemCheck(dto: AdminDashboardSystemCheckDto): AdminDashboardSystemCheck {
    return {
        key: dto.key,
        label: dto.label,
        status: dto.status,
        text: dto.text,
        icon: dto.icon,
    };
}

function mapSystemHealth(dto: AdminDashboardSystemHealthDto): AdminDashboardSystemHealth {
    return {
        status: dto.status,
        checks: dto.checks.map(mapSystemCheck),
    };
}

function mapQuickAction(dto: AdminDashboardQuickActionDto): AdminDashboardQuickAction {
    return {
        key: dto.key,
        label: dto.label,
        description: dto.description,
        icon: dto.icon,
        routeName: dto.route_name,
        tone: dto.tone,
    };
}
