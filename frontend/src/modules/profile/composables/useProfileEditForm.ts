import { onBeforeUnmount, onMounted, reactive, ref } from "vue";

import { mapEditFormToPayload } from "@/modules/profile/mappers/profile-edit.mapper";
import { isRussianPhoneComplete } from "@/modules/auth/composables/usePhoneMask";
import {
    getProfileEditPage,
    getProfileCitySuggestions,
    removeProfileAvatar,
    saveProfileAvatar,
    saveProfileEdit,
} from "@/modules/profile/services/profile-edit.service";
import type {
    ProfileEditFormErrors,
    ProfileCitySuggestion,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";
import type {
    CurrentProfileDto,
    ProfilePageModel,
} from "@/modules/profile/types/profile.types";
import { useAuthStore } from "@/stores/auth.store";

function createEmptyForm(): ProfileEditFormState {
    return {
        firstName: "",
        lastName: "",
        middleName: "",
        birthDate: "",
        gender: "not_specified",
        city: "",
        about: "",

        email: "",
        backupEmail: "",
        phone: "",
        vkUrl: "",
        maxUrl: "",
        preferredContactMethod: "email",

        showEmail: true,
        showPhone: false,
        emailNotifications: true,
        pushNotifications: true,

        roleProfile: {},
    };
}

function createEmptyErrors(): ProfileEditFormErrors {
    return {
        firstName: "",
        lastName: "",
        birthDate: "",
        phone: "",
        backupEmail: "",
        vkUrl: "",
        maxUrl: "",
        common: "",
    };
}

export function useProfileEditForm() {
    const authStore = useAuthStore();
    const source = ref<CurrentProfileDto | null>(null);
    const pageModel = ref<ProfilePageModel | null>(null);

    const form = reactive<ProfileEditFormState>(createEmptyForm());
    const errors = reactive<ProfileEditFormErrors>(createEmptyErrors());

    const isLoading = ref(false);
    const isSubmitting = ref(false);
    const isAvatarSubmitting = ref(false);
    const successMessage = ref("");
    const citySuggestions = ref<ProfileCitySuggestion[]>([]);
    const isCitySuggestionsLoading = ref(false);
    let citySuggestionsRequestId = 0;
    let citySuggestionsTimer: ReturnType<typeof setTimeout> | null = null;

    function setForm(nextForm: ProfileEditFormState): void {
        Object.assign(form, nextForm);
    }

    function clearErrors(): void {
        Object.assign(errors, createEmptyErrors());
    }

    function validateForm(): boolean {
        clearErrors();

        if (!form.firstName.trim()) {
            errors.firstName = "Укажите имя.";
        }

        if (!form.lastName.trim()) {
            errors.lastName = "Укажите фамилию.";
        }

        if (!isRussianPhoneComplete(form.phone)) {
            errors.phone = "Укажите номер телефона полностью.";
        }

        if (
            form.backupEmail.trim() &&
            form.backupEmail.trim().toLowerCase() === form.email.trim().toLowerCase()
        ) {
            errors.backupEmail = "Резервный email должен отличаться от основного.";
        }

        return (
            !errors.firstName &&
            !errors.lastName &&
            !errors.phone &&
            !errors.backupEmail
        );
    }

    function searchCities(query: string): void {
        if (citySuggestionsTimer) {
            clearTimeout(citySuggestionsTimer);
        }

        const normalizedQuery = query.trim();

        if (normalizedQuery.length < 2) {
            citySuggestions.value = [];
            isCitySuggestionsLoading.value = false;
            return;
        }

        citySuggestionsTimer = setTimeout(async () => {
            const requestId = ++citySuggestionsRequestId;
            isCitySuggestionsLoading.value = true;

            try {
                const suggestions = await getProfileCitySuggestions(normalizedQuery);

                if (requestId === citySuggestionsRequestId) {
                    citySuggestions.value = suggestions;
                }
            } catch {
                if (requestId === citySuggestionsRequestId) {
                    citySuggestions.value = [];
                }
            } finally {
                if (requestId === citySuggestionsRequestId) {
                    isCitySuggestionsLoading.value = false;
                }
            }
        }, 300);
    }

    function selectCity(suggestion: ProfileCitySuggestion): void {
        form.city = suggestion.value;
        citySuggestions.value = [];
    }

    async function loadProfileEdit(): Promise<void> {
        isLoading.value = true;
        successMessage.value = "";
        clearErrors();

        try {
            const result = await getProfileEditPage();

            source.value = result.source;
            pageModel.value = result.pageModel;
            setForm(result.form);
        } catch (error) {
            errors.common = getProfileEditErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    async function submitForm(): Promise<void> {
        if (!validateForm()) {
            return;
        }

        isSubmitting.value = true;
        successMessage.value = "";
        clearErrors();

        try {
            const result = await saveProfileEdit(mapEditFormToPayload(form));

            source.value = result.source;
            pageModel.value = result.pageModel;
            setForm(result.form);
            successMessage.value = "Профиль успешно обновлён.";
        } catch (error) {
            errors.common = getProfileEditErrorMessage(error);
        } finally {
            isSubmitting.value = false;
        }
    }

    async function uploadAvatar(file: File): Promise<void> {
        isAvatarSubmitting.value = true;
        successMessage.value = "";
        clearErrors();

        try {
            const result = await saveProfileAvatar(file);

            source.value = result.source;
            pageModel.value = result.pageModel;
            setForm(result.form);
            authStore.setAvatarUrl(result.source.identity.avatar_url);
            successMessage.value = "Аватар отправлен на обновление.";
        } catch (error) {
            errors.common = getProfileEditErrorMessage(error);
        } finally {
            isAvatarSubmitting.value = false;
        }
    }

    async function deleteAvatar(): Promise<void> {
        isAvatarSubmitting.value = true;
        successMessage.value = "";
        clearErrors();

        try {
            const result = await removeProfileAvatar();

            source.value = result.source;
            pageModel.value = result.pageModel;
            setForm(result.form);
            authStore.setAvatarUrl("");
            successMessage.value = "Аватар удалён.";
        } catch (error) {
            errors.common = getProfileEditErrorMessage(error);
        } finally {
            isAvatarSubmitting.value = false;
        }
    }

    onMounted(() => {
        void loadProfileEdit();
    });

    onBeforeUnmount(() => {
        if (citySuggestionsTimer) {
            clearTimeout(citySuggestionsTimer);
        }
    });

    return {
        source,
        pageModel,
        form,
        errors,
        isLoading,
        isSubmitting,
        isAvatarSubmitting,
        successMessage,
        citySuggestions,
        isCitySuggestionsLoading,
        loadProfileEdit,
        submitForm,
        uploadAvatar,
        deleteAvatar,
        searchCities,
        selectCity,
    };
}

function getProfileEditErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось сохранить изменения профиля.";
}
