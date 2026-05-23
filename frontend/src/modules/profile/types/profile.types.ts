import type {
    DashboardCalendarContent,
    DashboardCalendarDay,
    DashboardNotesContent,
    DashboardNotificationsContent,
    DashboardPageScaffoldModel,
    DashboardProfilePanelContent,
    DashboardShellConfig,
} from "@/components/dashboard/types/dashboard.types";

export type ProfileRoleCode =
    | "superadmin"
    | "director"
    | "org_admin"
    | "department_head"
    | "teacher"
    | "curator"
    | "methodist"
    | "organizer"
    | "mentor"
    | "learner"
    | "guardian"
    | string;

export interface CurrentProfileIdentityDto {
    id: number;
    email: string;
    phone: string;
    first_name: string;
    last_name: string;
    middle_name: string;
    full_name: string;
    birth_date: string | null;
    gender: string;
    city: string;
    about: string;
    avatar_url: string;
    timezone: string;
}

export interface CurrentProfileContactsDto {
    email: string;
    backup_email: string;
    phone: string;
    vk_url: string;
    max_url: string;
    preferred_contact_method: string;
    is_email_verified: boolean;
    is_phone_verified: boolean;
    show_email: boolean;
    show_phone: boolean;
}

export interface CurrentProfileDisplaySettingsDto {
    show_email: boolean;
    show_phone: boolean;
    email_notifications: boolean;
    push_notifications: boolean;
}

export interface CurrentProfileRoleDto {
    code: ProfileRoleCode;
    label: string;
}

export interface CurrentProfileDto {
    identity: CurrentProfileIdentityDto;
    contacts: CurrentProfileContactsDto;
    display_settings: CurrentProfileDisplaySettingsDto;
    active_role: CurrentProfileRoleDto;
    role_profile: Record<string, unknown>;
    available_roles: string[];
}

export interface ProfileIdentityModel {
    id: number;
    fullName: string;
    firstName: string;
    lastName: string;
    middleName: string;
    birthDate: string;
    gender: string;
    city: string;
    about: string;
    avatarUrl: string;
    timezone: string;
}

export interface ProfileContactItemModel {
    key: string;
    label: string;
    value: string;
    icon: string;
    href?: string;
    isVerified?: boolean;
    isVisible?: boolean;
}

export interface ProfileRoleModel {
    code: ProfileRoleCode;
    label: string;
    profile: Record<string, unknown>;
}

export interface ProfileHeroStatModel {
    value: string | number;
    label: string;
}

export interface ProfileHeroModel {
    topline: string;
    icon: string;
    title: string;
    text: string;
    avatarUrl: string;
    avatarAlt: string;
    roleLabel: string;
    subtitle: string;
    badges: {
        icon: string;
        label: string;
    }[];
    stats: ProfileHeroStatModel[];
}

export interface ProfileIdentityCardModel {
    title: string;
    text: string;
    facts: {
        label: string;
        value: string;
    }[];
}

export interface ProfileContactsCardModel {
    title: string;
    text: string;
    contacts: ProfileContactItemModel[];
    statuses: {
        label: string;
        value: string;
        isSuccess: boolean;
    }[];
}

export interface ProfileRoleSectionModel {
    roleCode: ProfileRoleCode;
    title: string;
    text: string;
    facts: {
        label: string;
        value: string;
    }[];
    tags: string[];
    groups: {
        title: string;
        text: string;
    }[];
    education: {
        title: string;
        text: string;
    }[];
}

export interface ProfilePageModel {
    scaffold: DashboardPageScaffoldModel;
    hero: ProfileHeroModel;
    identityCard: ProfileIdentityCardModel;
    contactsCard: ProfileContactsCardModel;
    roleSection: ProfileRoleSectionModel;
}

export interface ProfileEditHeroModel {
    topline: string;
    icon: string;
    title: string;
    text: string;
    badges: {
        icon: string;
        label: string;
    }[];
    primaryActionLabel: string;
    secondaryActionLabel: string;
    secondaryActionTo: {
        name: string;
    };
}

export interface ProfileRoleFieldModel {
    key: string;
    label: string;
    value: string | number | boolean;
    type: "text" | "number" | "textarea" | "checkbox";
    placeholder?: string;
}

export interface ProfileAchievementsStatModel {
    key: string;
    icon: string;
    value: string | number;
    label: string;
}

export interface ProfileAchievementDocumentModel {
    id: string | number;
    title: string;
    subtitle: string;
    icon: string;
    sourceLabel: string;
    categoryLabel: string;
    sourceType: "platform" | "personal";
    category: string;
    isFeatured?: boolean;
    previewLabel: string;
    downloadLabel: string;
}

export interface ProfileAchievementsPageModel {
    scaffold: DashboardPageScaffoldModel;
    hero: {
        topline: string;
        icon: string;
        title: string;
        text: string;
        badges: {
            icon: string;
            label: string;
        }[];
        statusRows: {
            label: string;
            value: string | number;
        }[];
    };
    stats: ProfileAchievementsStatModel[];
    filters: {
        sources: {
            key: string;
            label: string;
        }[];
        categories: {
            key: string;
            label: string;
        }[];
        uploadLabel: string;
    };
    featuredDocuments: ProfileAchievementDocumentModel[];
    documents: ProfileAchievementDocumentModel[];
}
