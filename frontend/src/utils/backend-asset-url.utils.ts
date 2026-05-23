import { API_CONFIG } from "@/app/config/api.config";

export function resolveBackendAssetUrl(value: string | undefined): string {
    if (!value) {
        return "";
    }

    try {
        const applicationOrigin = typeof window === "undefined"
            ? "http://localhost"
            : window.location.origin;
        const apiUrl = new URL(API_CONFIG.baseURL, applicationOrigin);

        return new URL(value, apiUrl).toString();
    } catch {
        return value;
    }
}
