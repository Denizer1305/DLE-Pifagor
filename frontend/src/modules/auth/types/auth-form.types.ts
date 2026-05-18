export interface AuthBadgeItem {
    icon: string;
    label: string;
}

export interface AuthMetaItem {
    icon: string;
    label: string;
}

export interface AuthIntroConfig {
    badges: AuthBadgeItem[];
    title: string;
    subtitle: string;
    meta: AuthMetaItem[];
}

export interface AuthFormCardConfig {
    icon: string;
    topline: string;
    title: string;
    description: string;
}

export type RegistrationRole = "learner" | "teacher" | "guardian";

export type RegistrationStep = 1 | 2;

export interface RegisterFormState {
    lastName: string;
    firstName: string;
    middleName: string;
    birthDate: string;
    email: string;
    phone: string;
    password: string;
    passwordConfirm: string;
    agreement: boolean;
}

export interface RegisterFormErrors {
    common: string;
    lastName: string;
    firstName: string;
    middleName: string;
    birthDate: string;
    email: string;
    phone: string;
    password: string;
    passwordConfirm: string;
    agreement: string;
}
