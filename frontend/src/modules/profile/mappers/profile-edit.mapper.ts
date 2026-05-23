import type {
    CurrentProfileEditPayload,
    ProfileCitySuggestion,
    ProfileCitySuggestionDto,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";
import type { CurrentProfileDto } from "@/modules/profile/types/profile.types";
import {
    formatRussianPhone,
    normalizeRussianPhone,
} from "@/modules/auth/composables/usePhoneMask";

export function mapCurrentProfileToEditForm(
    dto: CurrentProfileDto,
): ProfileEditFormState {
    return {
        firstName: dto.identity.first_name || "",
        lastName: dto.identity.last_name || "",
        middleName: dto.identity.middle_name || "",
        birthDate: dto.identity.birth_date || "",
        gender: dto.identity.gender || "not_specified",
        city: dto.identity.city || "",
        about: dto.identity.about || "",

        email: dto.identity.email || "",
        backupEmail: dto.contacts.backup_email || "",
        phone: formatRussianPhone(dto.contacts.phone || ""),
        vkUrl: dto.contacts.vk_url || "",
        maxUrl: dto.contacts.max_url || "",
        preferredContactMethod: normalizePreferredContactMethod(
            dto.contacts.preferred_contact_method,
        ),

        showEmail: dto.display_settings.show_email,
        showPhone: dto.display_settings.show_phone,
        emailNotifications: dto.display_settings.email_notifications,
        pushNotifications: dto.display_settings.push_notifications,

        roleProfile: normalizeRoleProfile(dto.role_profile),
    };
}

export function mapEditFormToPayload(
    form: ProfileEditFormState,
): CurrentProfileEditPayload {
    return {
        first_name: form.firstName.trim(),
        last_name: form.lastName.trim(),
        middle_name: form.middleName.trim(),
        birth_date: form.birthDate || null,
        gender: form.gender,
        city: form.city.trim(),
        about: form.about.trim(),

        backup_email: form.backupEmail.trim(),
        phone: normalizeRussianPhone(form.phone),
        vk_url: form.vkUrl.trim(),
        max_url: form.maxUrl.trim(),
        preferred_contact_method: form.preferredContactMethod,

        show_email: form.showEmail,
        show_phone: form.showPhone,
        email_notifications: form.emailNotifications,
        push_notifications: form.pushNotifications,

        role_profile: {
            ...form.roleProfile,
        },
    };
}

function normalizePreferredContactMethod(
    value: string,
): ProfileEditFormState["preferredContactMethod"] {
    if (
        value === "email" ||
        value === "phone" ||
        value === "vk" ||
        value === "max"
    ) {
        return value;
    }

    return "email";
}

export function mapProfileCitySuggestions(
    suggestions: ProfileCitySuggestionDto[],
): ProfileCitySuggestion[] {
    return suggestions.map((suggestion) => {
        return {
            value: suggestion.value,
            unrestrictedValue: suggestion.unrestricted_value,
        };
    });
}

function normalizeRoleProfile(
    value: Record<string, unknown>,
): ProfileEditFormState["roleProfile"] {
    return Object.fromEntries(
        Object.entries(value).filter(([, item]) => {
            return (
                typeof item === "string" ||
                typeof item === "number" ||
                item === null ||
                typeof item === "undefined"
            );
        }),
    ) as ProfileEditFormState["roleProfile"];
}
