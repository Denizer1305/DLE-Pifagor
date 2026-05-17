import axios, {
    AxiosError,
    type AxiosInstance,
    type AxiosRequestConfig,
} from "axios";

import { API_CONFIG } from "@/app/config/api.config";
import { normalizeApiError } from "./api.errors";

interface RetryableAxiosRequestConfig extends AxiosRequestConfig {
    _retry?: boolean;
}

interface RefreshResponse {
    access: string;
}

let accessToken: string | null = null;
let refreshPromise: Promise<string | null> | null = null;

export function setAccessToken(token: string | null): void {
    accessToken = token;
}

export function getAccessToken(): string | null {
    return accessToken;
}

function createHttpClient(): AxiosInstance {
    return axios.create({
        baseURL: API_CONFIG.baseURL,
        timeout: API_CONFIG.timeout,
        withCredentials: API_CONFIG.withCredentials,
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
    });
}

export const httpClient = createHttpClient();

const refreshClient = createHttpClient();

function isAuthRefreshRequest(config?: AxiosRequestConfig): boolean {
    return Boolean(config?.url?.includes("/users/auth/refresh/"));
}

function isAuthLoginRequest(config?: AxiosRequestConfig): boolean {
    return Boolean(config?.url?.includes("/users/auth/login/"));
}

function isAuthLogoutRequest(config?: AxiosRequestConfig): boolean {
    return Boolean(config?.url?.includes("/users/auth/logout/"));
}

async function requestNewAccessToken(): Promise<string | null> {
    if (!refreshPromise) {
        refreshPromise = refreshClient
            .post<RefreshResponse>("/users/auth/refresh/", {})
            .then((response) => {
                const token = response.data.access;

                setAccessToken(token);

                return token;
            })
            .catch(() => {
                setAccessToken(null);

                return null;
            })
            .finally(() => {
                refreshPromise = null;
            });
    }

    return refreshPromise;
}

httpClient.interceptors.request.use((config) => {
    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
});

httpClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as RetryableAxiosRequestConfig | undefined;
        const status = error.response?.status;

        if (
            status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            !isAuthRefreshRequest(originalRequest) &&
            !isAuthLoginRequest(originalRequest) &&
            !isAuthLogoutRequest(originalRequest)
        ) {
            originalRequest._retry = true;

            const newAccessToken = await requestNewAccessToken();

            if (newAccessToken) {
                originalRequest.headers = {
                    ...originalRequest.headers,
                    Authorization: `Bearer ${newAccessToken}`,
                };

                return httpClient(originalRequest);
            }
        }

        throw normalizeApiError(error);
    },
);
