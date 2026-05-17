export interface UserShort {
    id: number;
    email: string;
    phone: string;
    first_name: string;
    last_name: string;
    middle_name: string;
    full_name: string;
}

export interface UserDetail extends UserShort {
    birth_date: string | null;
    status: string;
    is_active: boolean;
    is_staff: boolean;
    is_email_verified: boolean;
    email_verified_at: string | null;
    is_phone_verified: boolean;
    phone_verified_at: string | null;
    is_login_allowed: boolean;
    account_managed_by: number | null;
    login_available_from: string | null;
    login_activation_requested_at: string | null;
    login_activated_at: string | null;
    scheduled_for_deletion_at: string | null;
    anonymized_at: string | null;
    created_at: string;
    updated_at: string;
}

export interface UserUpdatePayload {
    first_name?: string;
    last_name?: string;
    middle_name?: string;
    birth_date?: string | null;
}