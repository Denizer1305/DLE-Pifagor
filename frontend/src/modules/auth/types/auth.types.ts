import type { UserDetail } from "@/modules/users/types/user.types";

export interface LoginPayload {
    email: string;
    password: string;
}

export interface LoginResponse {
    user: UserDetail;
    access: string;
}

export interface RefreshResponse {
    access: string;
}

export interface EmailVerificationPayload {
    token: string;
}

export interface ForgotPasswordPayload {
    email: string;
}

export interface ForgotPasswordResponse {
    message: string;
}

export interface ResetPasswordPayload {
    token: string;
    password: string;
    password_confirm: string;
}

export interface ResetPasswordResponse {
    message: string;
}

export interface BaseRegistrationPayload {
    email: string;
    phone: string;
    password: string;
    first_name: string;
    last_name: string;
    middle_name?: string;
    birth_date?: string | null;
}

export interface TeacherRegistrationPayload extends BaseRegistrationPayload {
    invite_code: string;
    position?: string;
}

export interface LearnerRegistrationPayload extends BaseRegistrationPayload {}

export interface GuardianRegistrationPayload extends BaseRegistrationPayload {}

export interface MinorLearnerRegistrationPayload extends BaseRegistrationPayload {
    organization_id?: number | null;
    department_id?: number | null;
    group_id?: number | null;
    curator_id?: number | null;
    relation_type?: string;
}
