import { httpClient } from "@/services/api/http.client";
import type {
    EmailVerificationPayload,
    ForgotPasswordPayload,
    ForgotPasswordResponse,
    GuardianRegistrationPayload,
    LearnerRegistrationPayload,
    LoginPayload,
    LoginResponse,
    MinorLearnerRegistrationPayload,
    RefreshResponse,
    ResetPasswordPayload,
    ResetPasswordResponse,
    TeacherRegistrationPayload,
} from "@/modules/auth/types/auth.types";
import type { UserDetail } from "@/modules/users/types/user.types";

const AUTH_BASE_URL = "/users/auth";

export async function login(payload: LoginPayload): Promise<LoginResponse> {
    const response = await httpClient.post<LoginResponse>(`${AUTH_BASE_URL}/login/`, payload);

    return response.data;
}

export async function refresh(): Promise<RefreshResponse> {
    const response = await httpClient.post<RefreshResponse>(`${AUTH_BASE_URL}/refresh/`, {});

    return response.data;
}

export async function logout(): Promise<void> {
    await httpClient.post(`${AUTH_BASE_URL}/logout/`);
}

export async function verifyEmail(payload: EmailVerificationPayload): Promise<UserDetail> {
    const response = await httpClient.post<UserDetail>(`${AUTH_BASE_URL}/verify-email/`, payload);

    return response.data;
}

export async function forgotPassword(payload: ForgotPasswordPayload): Promise<ForgotPasswordResponse> {
    const response = await httpClient.post<ForgotPasswordResponse>(
        `${AUTH_BASE_URL}/password/forgot/`,
        payload,
    );

    return response.data;
}

export async function resetPassword(payload: ResetPasswordPayload): Promise<ResetPasswordResponse> {
    const response = await httpClient.post<ResetPasswordResponse>(
        `${AUTH_BASE_URL}/password/reset/`,
        payload,
    );

    return response.data;
}

export async function registerTeacher(payload: TeacherRegistrationPayload): Promise<UserDetail> {
    const response = await httpClient.post<UserDetail>(`${AUTH_BASE_URL}/register/teacher/`, payload);

    return response.data;
}

export async function registerLearner(payload: LearnerRegistrationPayload): Promise<UserDetail> {
    const response = await httpClient.post<UserDetail>(`${AUTH_BASE_URL}/register/learner/`, payload);

    return response.data;
}

export async function registerGuardian(payload: GuardianRegistrationPayload): Promise<UserDetail> {
    const response = await httpClient.post<UserDetail>(`${AUTH_BASE_URL}/register/guardian/`, payload);

    return response.data;
}

export async function registerMinorLearner(payload: MinorLearnerRegistrationPayload): Promise<UserDetail> {
    const response = await httpClient.post<UserDetail>(`${AUTH_BASE_URL}/register/minor-learner/`, payload);

    return response.data;
}