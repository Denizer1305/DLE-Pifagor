export const API_CONFIG = {
    baseURL: (import.meta as any).env?.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
    timeout: 15000,
    withCredentials: true,
} as const;
