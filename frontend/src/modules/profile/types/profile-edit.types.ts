import type { CurrentProfileDto } from "@/modules/profile/types/profile.types";

export interface CurrentProfileEditPayload {
    first_name?: string;
    last_name?: string;
    middle_name?: string;
    birth_date?: string | null;
    gender?: string;
    city?: string;
    about?: string;

    phone?: string;
    backup_email?: string;
    vk_url?: string;
    max_url?: string;
    preferred_contact_method?: "email" | "phone" | "vk" | "max";

    show_email?: boolean;
    show_phone?: boolean;
    email_notifications?: boolean;
    push_notifications?: boolean;

    role_profile?: Record<string, unknown>;
}

export interface ProfileEditFormState {
    firstName: string;
    lastName: string;
    middleName: string;
    birthDate: string;
    gender: string;
    city: string;
    about: string;

    email: string;
    backupEmail: string;
    phone: string;
    vkUrl: string;
    maxUrl: string;
    preferredContactMethod: "email" | "phone" | "vk" | "max";

    showEmail: boolean;
    showPhone: boolean;
    emailNotifications: boolean;
    pushNotifications: boolean;

    roleProfile: Record<string, string | number | null | undefined>;
}

export interface ProfileEditFormErrors {
    firstName: string;
    lastName: string;
    birthDate: string;
    phone: string;
    backupEmail: string;
    vkUrl: string;
    maxUrl: string;
    common: string;
}

export interface ProfileEditPageState {
    source: CurrentProfileDto | null;
    form: ProfileEditFormState;
}

export interface ProfileCitySuggestion {
    value: string;
    unrestrictedValue: string;
}

export interface ProfileCitySuggestionDto {
    value: string;
    unrestricted_value: string;
}

export interface ProfileEditActionContent {
    label: string;
    icon?: string;
    pendingLabel?: string;
    to?: {
        name: string;
    };
}

export interface ProfileEditHeroContent {
    icon: string;
    topline: string;
    title: string;
    text: string;
    badges: {
        icon: string;
        label: string;
    }[];
    primaryAction: ProfileEditActionContent;
    secondaryAction: ProfileEditActionContent;
}

export interface ProfileEditSubmitContent {
    title: string;
    text: string;
    cancelAction: ProfileEditActionContent;
    submitAction: ProfileEditActionContent;
}

export interface ProfileEditPageContent {
    hero: ProfileEditHeroContent;
    submit: ProfileEditSubmitContent;
    successTitle: string;
    successIcon: string;
}

export interface ProfileEditSectionHeading {
    icon: string;
    topline: string;
    title: string;
    text: string;
}

export interface ProfileEditSelectOption {
    value: string;
    label: string;
}

export interface ProfileEditFormContent {
    identity: {
        heading: ProfileEditSectionHeading;
        labels: Record<"lastName" | "firstName" | "middleName" | "birthDate" | "gender" | "city" | "about", string>;
        aboutPlaceholder: string;
        genderAriaLabel: string;
        genderOptions: ProfileEditSelectOption[];
    };
    contacts: {
        heading: ProfileEditSectionHeading;
        labels: Record<"email" | "phone" | "backupEmail" | "vkUrl" | "maxUrl" | "preferredContactMethod", string>;
        emailStatus: string;
        phonePlaceholder: string;
        backupEmailPlaceholder: string;
        contactMethodAriaLabel: string;
        contactMethodOptions: ProfileEditSelectOption[];
    };
    display: {
        heading: ProfileEditSectionHeading;
        toggles: {
            key: "showEmail" | "showPhone" | "emailNotifications" | "pushNotifications";
            label: string;
            text: string;
        }[];
    };
}
