<script setup lang="ts">
import ProfileEditContactsSection from "@/modules/profile/components/ProfileEditContactsSection.vue";
import ProfileEditDisplaySection from "@/modules/profile/components/ProfileEditDisplaySection.vue";
import ProfileEditIdentitySection from "@/modules/profile/components/ProfileEditIdentitySection.vue";
import { profileEditFormContent } from "@/modules/profile/data/profile-edit.data";
import type {
    ProfileCitySuggestion,
    ProfileEditFormErrors,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";

interface Props {
    form: ProfileEditFormState;
    errors: ProfileEditFormErrors;
    citySuggestions: ProfileCitySuggestion[];
    isCitySuggestionsLoading?: boolean;
}

interface Emits {
    (event: "search-city", value: string): void;
    (event: "select-city", suggestion: ProfileCitySuggestion): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <ProfileEditIdentitySection
        :form="form"
        :errors="errors"
        :content="profileEditFormContent.identity"
        :city-suggestions="citySuggestions"
        :is-city-suggestions-loading="isCitySuggestionsLoading"
        @search-city="emit('search-city', $event)"
        @select-city="emit('select-city', $event)"
    />

    <ProfileEditContactsSection
        :form="form"
        :errors="errors"
        :content="profileEditFormContent.contacts"
    />

    <ProfileEditDisplaySection
        :form="form"
        :content="profileEditFormContent.display"
    />
</template>
