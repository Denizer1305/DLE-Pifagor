import axios, {
    AxiosError,
    AxiosHeaders,
    type AxiosInstance,
    type AxiosRequestConfig,
} from "axios";

import { API_CONFIG } from "@/app/config/api.config";
import { normalizeApiError } from "@/services/api/api.errors";

interface RetryableAxiosRequestConfig extends AxiosRequestConfig {
    _retry?: boolean;
}

interface RefreshResponse {
    access: string;
}

const ACCESS_TOKEN_STORAGE_KEY = "pifagor_access_token";
const LOGIN_PATH = "/login";

let accessToken: string | null = readAccessTokenFromStorage();
let refreshPromise: Promise<string | null> | null = null;

function readAccessTokenFromStorage(): string | null {
    try {
        return window.localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY);
    } catch {
        return null;
    }
}

function writeAccessTokenToStorage(token: string | null): void {
    try {
        if (token) {
            window.localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, token);
            return;
        }

        window.localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY);
    } catch {
        // localStorage может быть недоступен в приватном режиме или тестах.
    }
}

export function setAccessToken(token: string | null): void {
    accessToken = token;
    writeAccessTokenToStorage(token);
}

export function getAccessToken(): string | null {
    return accessToken || readAccessTokenFromStorage();
}

export function clearAccessToken(): void {
    setAccessToken(null);
}

function redirectToLogin(): void {
    if (typeof window === "undefined") {
        return;
    }

    const currentPath = `${window.location.pathname}${window.location.search}`;

    if (window.location.pathname === LOGIN_PATH) {
        return;
    }

    const loginUrl = new URL(LOGIN_PATH, window.location.origin);

    if (currentPath && currentPath !== "/") {
        loginUrl.searchParams.set("redirect", currentPath);
    }

    window.location.assign(loginUrl.toString());
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

function getRequestUrl(config?: AxiosRequestConfig): string {
    return config?.url || "";
}

function isAuthRefreshRequest(config?: AxiosRequestConfig): boolean {
    return getRequestUrl(config).includes("/users/auth/refresh/");
}

function isAuthLoginRequest(config?: AxiosRequestConfig): boolean {
    return getRequestUrl(config).includes("/users/auth/login/");
}

function isAuthRegisterRequest(config?: AxiosRequestConfig): boolean {
    return getRequestUrl(config).includes("/users/auth/register/");
}

function isAuthLogoutRequest(config?: AxiosRequestConfig): boolean {
    return getRequestUrl(config).includes("/users/auth/logout/");
}

function isAuthRequest(config?: AxiosRequestConfig): boolean {
    return (
        isAuthRefreshRequest(config) ||
        isAuthLoginRequest(config) ||
        isAuthRegisterRequest(config) ||
        isAuthLogoutRequest(config)
    );
}

function setAuthorizationHeader(
    config: AxiosRequestConfig,
    token: string,
): void {
    if (!config.headers) {
        config.headers = new AxiosHeaders();
    }

    if (config.headers instanceof AxiosHeaders) {
        config.headers.set("Authorization", `Bearer ${token}`);
        return;
    }

    config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
    };
}

async function requestNewAccessToken(redirectOnFail = false): Promise<string | null> {
    if (!refreshPromise) {
        refreshPromise = refreshClient
            .post<RefreshResponse>("/users/auth/refresh/", {})
            .then((response) => {
                const token = response.data.access;

                setAccessToken(token);

                return token;
            })
            .catch(() => {
                clearAccessToken();

                return null;
            })
            .finally(() => {
                refreshPromise = null;
            });
    }

    const token = await refreshPromise;

    if (!token && redirectOnFail) {
        redirectToLogin();
    }

    return token;
}

export async function refreshAccessToken(): Promise<string | null> {
    return requestNewAccessToken();
}

httpClient.interceptors.request.use((config) => {
    const token = getAccessToken();

    if (token) {
        setAuthorizationHeader(config, token);
    }

    if (config.data instanceof FormData && config.headers instanceof AxiosHeaders) {
        config.headers.delete("Content-Type");
    }

    return config;
});

httpClient.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error: AxiosError) => {
        const originalRequest = error.config as RetryableAxiosRequestConfig | undefined;
        const status = error.response?.status;

        if (
            status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            !isAuthRequest(originalRequest)
        ) {
            originalRequest._retry = true;

            const newAccessToken = await requestNewAccessToken(true);

            if (newAccessToken) {
                setAuthorizationHeader(originalRequest, newAccessToken);

                return httpClient(originalRequest);
            }
        }

        throw normalizeApiError(error);
    },
);
