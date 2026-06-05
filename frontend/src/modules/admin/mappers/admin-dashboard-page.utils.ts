import type { AdminDashboardSummary } from "@/modules/admin/types/admin-dashboard.types";

export function getSummaryStatValue(summary: AdminDashboardSummary, key: string): number {
    return summary.stats.find((stat) => stat.key === key)?.value ?? 0;
}

export function getSummaryStatCaption(
    summary: AdminDashboardSummary,
    key: string,
    fallback: string,
): string {
    return summary.stats.find((stat) => stat.key === key)?.caption || fallback;
}

export function getSharePercent(value: number, total: number): number {
    if (total <= 0 || value <= 0) {
        return 0;
    }

    return Math.min(100, Math.round((value / total) * 100));
}

export function getSystemHealthScore(status: string): number {
    if (status === "critical") {
        return 40;
    }

    return status === "warning" ? 70 : 100;
}

export function getSystemHealthText(status: string): string {
    if (status === "critical") {
        return "Backend сообщает о критическом состоянии системы.";
    }

    if (status === "warning") {
        return "Backend сообщает, что системе требуется внимание.";
    }

    return "Backend сообщает, что система работает стабильно.";
}

export function formatAdminNumber(value: number): string {
    return new Intl.NumberFormat("ru-RU").format(value);
}
